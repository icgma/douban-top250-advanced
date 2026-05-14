"""
爬虫核心模块
"""

from .async_scraper import AsyncDoubanScraper
from .data_parser import MovieParser

__all__ = ['AsyncDoubanScraper', 'MovieParser']
