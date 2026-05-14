"""
异步爬虫主模块 - 使用aiohttp实现并发爬取
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Optional
from pathlib import Path
from tqdm import tqdm
from config import ScraperConfig
from utils.logger import logger
from utils.helpers import calculate_progress
from scraper.data_parser import MovieParser
from scraper.anti_crawl import anti_crawl


class AsyncDoubanScraper:
    """
    异步豆瓣电影爬虫
    
    功能：
    - 使用aiohttp实现异步并发请求
    - 支持断点续传
    - 智能重试机制
    - 进度显示
    """
    
    def __init__(self):
        """初始化爬虫"""
        self.all_movies = []
        self.session = None
        self.checkpoint_file = ScraperConfig.CHECKPOINT_FILE
        logger.info("异步豆瓣爬虫初始化完成")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        connector = aiohttp.TCPConnector(
            limit=ScraperConfig.MAX_CONCURRENT_REQUESTS,
            ssl=False
        )
        timeout = aiohttp.ClientTimeout(total=ScraperConfig.REQUEST_TIMEOUT)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            logger.info("会话已关闭")
    
    async def fetch_page(self, url: str, page_num: int, retry_count: int = 0) -> Optional[str]:
        """
        异步获取单个页面
        
        Args:
            url: 请求URL
            page_num: 页面号
            retry_count: 当前重试次数
        
        Returns:
            HTML内容字符串
        """
        headers = anti_crawl.get_random_headers()
        
        try:
            # 智能延迟
            await anti_crawl.smart_delay(page_num)
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text(encoding='utf-8')
                    logger.debug(f"第{page_num}页获取成功")
                    return html
                elif response.status == 403:
                    logger.warning(f"第{page_num}页被禁止访问 (403)")
                    return None
                else:
                    logger.warning(f"第{page_num}页请求失败，状态码: {response.status}")
                    return None
        
        except asyncio.TimeoutError:
            logger.warning(f"第{page_num}页请求超时")
        except Exception as e:
            logger.error(f"第{page_num}页请求异常: {e}")
        
        # 重试逻辑
        if retry_count < ScraperConfig.MAX_RETRIES:
            logger.info(f"第{page_num}页重试 ({retry_count + 1}/{ScraperConfig.MAX_RETRIES})")
            await asyncio.sleep(ScraperConfig.RETRY_DELAY)
            return await self.fetch_page(url, page_num, retry_count + 1)
        
        return None
    
    async def scrape_single_page(self, page_num: int) -> List[Dict]:
        """
        爬取单个页面并解析
        
        Args:
            page_num: 页面号 (0-9)
        
        Returns:
            电影数据列表
        """
        start = page_num * ScraperConfig.MOVIES_PER_PAGE
        url = f"{ScraperConfig.BASE_URL}?start={start}&filter="
        
        logger.info(f"开始爬取第 {page_num + 1}/10 页 (start={start})")
        
        html = await self.fetch_page(url, page_num)
        
        if not html:
            logger.error(f"第 {page_num + 1} 页获取失败")
            return []
        
        # 解析电影数据
        movies = MovieParser.parse_movie_list(html)
        movies = MovieParser.validate_and_clean(movies)
        
        return movies
    
    async def scrape_all_pages(self) -> List[Dict]:
        """
        爬取所有页面（并发执行）
        
        Returns:
            所有电影数据列表
        """
        logger.info("=" * 60)
        logger.info("开始爬取豆瓣Top 250电影")
        logger.info("=" * 60)
        
        # 检查断点续传
        start_page = self._load_checkpoint()
        
        tasks = []
        for page_num in range(start_page, ScraperConfig.TOTAL_PAGES):
            task = asyncio.create_task(self.scrape_single_page(page_num))
            tasks.append(task)
        
        # 并发执行所有任务
        results = await asyncio.gather(*tasks)
        
        # 合并结果
        for movies in results:
            self.all_movies.extend(movies)
        
        # 按排名排序
        self.all_movies.sort(key=lambda x: x['rank'])
        
        logger.info(f"\n爬取完成！共获取 {len(self.all_movies)} 部电影")
        
        # 保存断点
        self._save_checkpoint(ScraperConfig.TOTAL_PAGES)
        
        return self.all_movies
    
    def _load_checkpoint(self) -> int:
        """
        加载断点信息
        
        Returns:
            起始页面号
        """
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    completed_pages = data.get('completed_pages', 0)
                    logger.info(f"从断点恢复：已完成 {completed_pages} 页")
                    return completed_pages
            except Exception as e:
                logger.warning(f"加载断点失败: {e}")
        
        return 0
    
    def _save_checkpoint(self, completed_pages: int):
        """
        保存断点信息
        
        Args:
            completed_pages: 已完成的页面数
        """
        try:
            checkpoint_data = {
                'completed_pages': completed_pages,
                'total_movies': len(self.all_movies),
                'timestamp': str(asyncio.get_event_loop().time())
            }
            
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"断点已保存：完成 {completed_pages} 页")
        except Exception as e:
            logger.warning(f"保存断点失败: {e}")
    
    def get_statistics(self) -> Dict:
        """
        获取爬取统计信息
        
        Returns:
            统计信息字典
        """
        if not self.all_movies:
            return {}
        
        stats = {
            'total_movies': len(self.all_movies),
            'avg_rating': sum(m['rating'] for m in self.all_movies) / len(self.all_movies),
            'max_rating': max(m['rating'] for m in self.all_movies),
            'min_rating': min(m['rating'] for m in self.all_movies),
            'years_range': {
                'earliest': min((m['year'] for m in self.all_movies if m['year']), default='N/A'),
                'latest': max((m['year'] for m in self.all_movies if m['year']), default='N/A'),
            }
        }
        
        return stats


async def run_scraper():
    """
    运行爬虫的主函数
    
    Returns:
        电影数据列表
    """
    async with AsyncDoubanScraper() as scraper:
        movies = await scraper.scrape_all_pages()
        
        # 打印统计信息
        stats = scraper.get_statistics()
        if stats:
            logger.info("\n" + "=" * 60)
            logger.info("爬取统计")
            logger.info("=" * 60)
            logger.info(f"总电影数: {stats['total_movies']}")
            logger.info(f"平均评分: {stats['avg_rating']:.2f}")
            logger.info(f"最高评分: {stats['max_rating']}")
            logger.info(f"最低评分: {stats['min_rating']}")
            logger.info(f"年代范围: {stats['years_range']['earliest']} - {stats['years_range']['latest']}")
        
        return movies


if __name__ == "__main__":
    # 直接运行测试
    asyncio.run(run_scraper())
