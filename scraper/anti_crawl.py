"""
反爬策略模块 - 实现多种反爬虫对抗技术
"""

import random
import asyncio
from fake_useragent import UserAgent
from config import ScraperConfig
from utils.logger import logger


class AntiCrawlStrategy:
    """
    反爬策略管理器
    
    功能：
    - 随机User-Agent轮换
    - 智能延迟控制
    - 请求头伪装
    """
    
    def __init__(self):
        """初始化反爬策略"""
        self.ua = UserAgent()
        self.request_count = 0
        logger.info("反爬策略初始化完成")
    
    def get_random_headers(self) -> dict:
        """
        生成随机请求头
        
        Returns:
            包含随机User-Agent的请求头字典
        """
        headers = ScraperConfig.DEFAULT_HEADERS.copy()
        headers['User-Agent'] = self.ua.random
        
        # 随机添加一些额外的请求头
        if random.random() > 0.5:
            headers['Referer'] = 'https://movie.douban.com/'
        
        if random.random() > 0.7:
            headers['Cache-Control'] = random.choice([
                'max-age=0',
                'no-cache',
                'no-store'
            ])
        
        return headers
    
    async def smart_delay(self, page_num: int = None):
        """
        智能延迟，根据请求次数和页面号动态调整延迟
        
        Args:
            page_num: 当前页面号（可选）
        """
        self.request_count += 1
        
        # 基础延迟
        delay = random.uniform(ScraperConfig.MIN_DELAY, ScraperConfig.MAX_DELAY)
        
        # 随着请求次数增加，适当增加延迟（模拟人类行为）
        if self.request_count > 20:
            delay *= 1.2
        if self.request_count > 50:
            delay *= 1.5
        
        # 页面间的固定延迟
        if page_num is not None and page_num > 0:
            delay = max(delay, ScraperConfig.DELAY_BETWEEN_PAGES)
        
        logger.debug(f"智能延迟: {delay:.2f}秒 (请求次数: {self.request_count})")
        await asyncio.sleep(delay)
    
    def get_rotating_proxy(self, proxy_list: list = None) -> dict:
        """
        从代理列表中随机选择一个代理
        
        Args:
            proxy_list: 代理列表
        
        Returns:
            代理字典，格式: {'http': 'proxy_url', 'https': 'proxy_url'}
        """
        if not proxy_list:
            return {}
        
        proxy = random.choice(proxy_list)
        return {
            'http': proxy,
            'https': proxy
        }
    
    def reset_counter(self):
        """重置请求计数器"""
        self.request_count = 0
        logger.info("请求计数器已重置")


# 全局反爬策略实例
anti_crawl = AntiCrawlStrategy()
