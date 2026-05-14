"""
CSV存储模块
"""

import csv
from typing import List, Dict
from pathlib import Path
from config import ScraperConfig
from utils.logger import logger


class CSVStorage:
    """CSV文件存储类"""
    
    def __init__(self, filepath: Path = None):
        """
        初始化CSV存储器
        
        Args:
            filepath: CSV文件路径
        """
        self.filepath = filepath or ScraperConfig.CSV_FILE
    
    def save(self, movies: List[Dict]):
        """
        保存电影数据到CSV文件
        
        Args:
            movies: 电影数据列表
        """
        if not movies:
            logger.warning("没有数据可保存")
            return
        
        # 确保目录存在
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # 获取所有字段名
        fieldnames = movies[0].keys()
        
        try:
            with open(self.filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movies)
            
            logger.info(f"✅ CSV文件已保存: {self.filepath}")
            logger.info(f"   共保存 {len(movies)} 条记录")
        
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")
            raise
