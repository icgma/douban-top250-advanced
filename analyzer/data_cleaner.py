"""
数据清洗模块
"""

import pandas as pd
from typing import List, Dict
from utils.logger import logger


class DataCleaner:
    """
    数据清洗器
    
    功能：
    - 去除重复数据
    - 处理缺失值
    - 数据类型转换
    - 异常值检测
    """
    
    def __init__(self, movies: List[Dict]):
        """
        初始化数据清洗器
        
        Args:
            movies: 原始电影数据列表
        """
        self.df = pd.DataFrame(movies)
        logger.info(f"加载原始数据: {len(self.df)} 条记录")
    
    def clean(self) -> pd.DataFrame:
        """
        执行完整的数据清洗流程
        
        Returns:
            清洗后的DataFrame
        """
        logger.info("开始数据清洗...")
        
        # 1. 去除完全重复的行
        self._remove_duplicates()
        
        # 2. 处理缺失值
        self._handle_missing_values()
        
        # 3. 数据类型转换
        self._convert_types()
        
        # 4. 去除异常值
        self._remove_outliers()
        
        logger.info(f"数据清洗完成，剩余 {len(self.df)} 条记录")
        return self.df
    
    def _remove_duplicates(self):
        """去除重复数据（基于rank）"""
        before_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=['rank'], keep='first')
        after_count = len(self.df)
        
        if before_count != after_count:
            logger.info(f"去除重复数据: {before_count} -> {after_count}")
    
    def _handle_missing_values(self):
        """处理缺失值"""
        # 对于数值型字段，用0填充
        numeric_cols = ['rating', 'rating_people']
        for col in numeric_cols:
            if col in self.df.columns:
                missing_count = self.df[col].isna().sum()
                if missing_count > 0:
                    self.df[col] = self.df[col].fillna(0)
                    logger.info(f"字段 '{col}' 填充 {missing_count} 个缺失值")
        
        # 对于文本字段，用空字符串填充
        text_cols = ['title', 'director', 'year', 'country', 'genre', 'quote']
        for col in text_cols:
            if col in self.df.columns:
                missing_count = self.df[col].isna().sum()
                if missing_count > 0:
                    self.df[col] = self.df[col].fillna('')
    
    def _convert_types(self):
        """数据类型转换"""
        # 确保数值类型正确
        if 'rating' in self.df.columns:
            self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce').fillna(0)
        
        if 'rating_people' in self.df.columns:
            self.df['rating_people'] = pd.to_numeric(self.df['rating_people'], errors='coerce').fillna(0).astype(int)
        
        if 'rank' in self.df.columns:
            self.df['rank'] = pd.to_numeric(self.df['rank'], errors='coerce').fillna(0).astype(int)
        
        logger.info("数据类型转换完成")
    
    def _remove_outliers(self):
        """去除异常值"""
        # 评分范围检查 (0-10)
        if 'rating' in self.df.columns:
            before_count = len(self.df)
            self.df = self.df[(self.df['rating'] >= 0) & (self.df['rating'] <= 10)]
            after_count = len(self.df)
            
            if before_count != after_count:
                logger.warning(f"去除 {before_count - after_count} 条评分异常记录")
        
        # 排名范围检查 (1-250)
        if 'rank' in self.df.columns:
            before_count = len(self.df)
            self.df = self.df[(self.df['rank'] >= 1) & (self.df['rank'] <= 250)]
            after_count = len(self.df)
            
            if before_count != after_count:
                logger.warning(f"去除 {before_count - after_count} 条排名异常记录")
