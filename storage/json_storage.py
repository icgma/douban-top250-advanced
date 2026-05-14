"""
JSON存储模块
"""

import json
from typing import List, Dict
from pathlib import Path
from config import ScraperConfig
from utils.logger import logger


class JSONStorage:
    """JSON文件存储类"""
    
    def __init__(self, filepath: Path = None):
        """
        初始化JSON存储器
        
        Args:
            filepath: JSON文件路径
        """
        self.filepath = filepath or ScraperConfig.JSON_FILE
    
    def save(self, movies: List[Dict]):
        """
        保存电影数据到JSON文件
        
        Args:
            movies: 电影数据列表
        """
        if not movies:
            logger.warning("没有数据可保存")
            return
        
        # 确保目录存在
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(movies, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ JSON文件已保存: {self.filepath}")
            logger.info(f"   共保存 {len(movies)} 条记录")
        
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            raise
