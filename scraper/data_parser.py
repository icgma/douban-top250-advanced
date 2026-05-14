"""
数据解析器模块 - 解析豆瓣电影页面HTML
"""

import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from utils.logger import logger
from utils.helpers import format_number, extract_year


class MovieParser:
    """
    电影数据解析器
    
    功能：
    - 解析HTML页面提取电影信息
    - 提取丰富的字段（片名、评分、导演、演员、年份等）
    - 数据清洗和格式化
    """
    
    @staticmethod
    def parse_movie_list(html: str) -> List[Dict]:
        """
        解析一页电影列表（25部电影）
        
        Args:
            html: 页面HTML内容
        
        Returns:
            电影数据字典列表
        """
        soup = BeautifulSoup(html, 'html.parser')
        movies = []
        
        # 查找所有电影项
        items = soup.select('div.item')
        
        for item in items:
            try:
                movie = MovieParser._parse_single_movie(item)
                if movie:
                    movies.append(movie)
            except Exception as e:
                logger.warning(f"解析单部电影失败: {e}")
                continue
        
        logger.info(f"本页解析到 {len(movies)} 部电影")
        return movies
    
    @staticmethod
    def _parse_single_movie(item) -> Optional[Dict]:
        """
        解析单个电影项
        
        Args:
            item: BeautifulSoup元素
        
        Returns:
            电影数据字典
        """
        try:
            # 排名
            rank_elem = item.select_one('em')
            rank = int(rank_elem.get_text(strip=True)) if rank_elem else 0
            
            # 片名（中文）
            title_elem = item.select_one('span.title')
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # 其他片名（英文/原名）
            other_titles = []
            for span in item.select('span.title')[1:]:
                text = span.get_text(strip=True)
                if text and text != '/':
                    other_titles.append(text)
            
            # 评分
            rating_elem = item.select_one('span.rating_num')
            rating = float(rating_elem.get_text(strip=True)) if rating_elem else 0.0
            
            # 评价人数
            people_elem = item.select_one('div.star span:last-child')
            rating_people = 0
            if people_elem:
                people_text = people_elem.get_text(strip=True)
                rating_people = format_number(people_text)
            
            # 一句话短评
            quote_elem = item.select_one('span.inq')
            quote = quote_elem.get_text(strip=True) if quote_elem else ""
            
            # 详细信息（导演、年份、国家、类型）
            info_p = item.select_one('div.bd p')
            director = ""
            year = ""
            country = ""
            genre = ""
            
            if info_p:
                lines = info_p.get_text(separator='\n').strip().split('\n')
                
                # 第一行：导演和主演
                if lines:
                    director_match = re.search(r'导演:\s*([^/]+?)(?:\s*主演:|$)', lines[0])
                    if director_match:
                        director = director_match.group(1).strip()
                
                # 最后一行：年份 / 国家 / 类型
                if len(lines) > 1:
                    info_line = lines[-1].strip()
                    parts = [p.strip() for p in info_line.split('/')]
                    
                    if len(parts) >= 1:
                        year = extract_year(parts[0])
                    if len(parts) >= 2:
                        country = parts[1].strip()
                    if len(parts) >= 3:
                        genre = parts[2].strip()
            
            # 海报图片
            img_elem = item.select_one('img')
            poster = img_elem['src'] if img_elem and img_elem.has_attr('src') else ""
            
            # 详情链接
            link_elem = item.select_one('div.hd a')
            link = link_elem['href'] if link_elem and link_elem.has_attr('href') else ""
            
            movie_data = {
                'rank': rank,
                'title': title,
                'other_titles': ' / '.join(other_titles) if other_titles else "",
                'rating': rating,
                'rating_people': rating_people,
                'quote': quote,
                'director': director,
                'year': year,
                'country': country,
                'genre': genre,
                'poster': poster,
                'link': link,
            }
            
            return movie_data
            
        except Exception as e:
            logger.error(f"解析电影项时出错: {e}")
            return None
    
    @staticmethod
    def validate_and_clean(movies: List[Dict]) -> List[Dict]:
        """
        验证并清洗电影数据
        
        Args:
            movies: 原始电影数据列表
        
        Returns:
            清洗后的电影数据列表
        """
        cleaned = []
        
        for movie in movies:
            # 跳过无效数据
            if not movie.get('rank') or not movie.get('title'):
                continue
            
            # 确保数据类型正确
            try:
                movie['rank'] = int(movie['rank'])
                movie['rating'] = float(movie['rating'])
                movie['rating_people'] = int(movie.get('rating_people', 0))
            except (ValueError, TypeError):
                continue
            
            cleaned.append(movie)
        
        logger.info(f"数据清洗: {len(movies)} -> {len(cleaned)} 部有效电影")
        return cleaned
