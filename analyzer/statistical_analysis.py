"""
统计分析模块
"""

import pandas as pd
from typing import Dict
from utils.logger import logger


class StatisticalAnalyzer:
    """
    统计分析器
    
    功能：
    - 基础统计信息
    - 评分分布分析
    - 年代趋势分析
    - 国家/地区分布
    - 导演作品分析
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        初始化统计分析器
        
        Args:
            df: 清洗后的电影数据DataFrame
        """
        self.df = df
        logger.info("统计分析器初始化完成")
    
    def basic_statistics(self) -> Dict:
        """
        计算基础统计信息
        
        Returns:
            统计信息字典
        """
        stats = {
            'total_movies': len(self.df),
            'avg_rating': self.df['rating'].mean(),
            'median_rating': self.df['rating'].median(),
            'max_rating': self.df['rating'].max(),
            'min_rating': self.df['rating'].min(),
            'std_rating': self.df['rating'].std(),
            'total_votes': self.df['rating_people'].sum(),
            'avg_votes': self.df['rating_people'].mean(),
        }
        
        logger.info("基础统计信息计算完成")
        return stats
    
    def rating_distribution(self) -> pd.Series:
        """
        评分分布分析
        
        Returns:
            评分段计数
        """
        # 定义评分段
        bins = [0, 8.0, 8.5, 9.0, 10]
        labels = ['<8.0', '8.0-8.4', '8.5-8.9', '9.0+']
        
        self.df['rating_bracket'] = pd.cut(self.df['rating'], bins=bins, labels=labels)
        distribution = self.df['rating_bracket'].value_counts().sort_index()
        
        logger.info("评分分布分析完成")
        return distribution
    
    def year_trend(self) -> pd.Series:
        """
        年代趋势分析
        
        Returns:
            各年代电影数量
        """
        # 提取有效年份
        valid_years = self.df[self.df['year'] != '']['year']
        
        # 转换为数值型
        valid_years = pd.to_numeric(valid_years, errors='coerce').dropna()
        
        # 按年代分组
        decades = (valid_years // 10 * 10).astype(int)
        decade_counts = decades.value_counts().sort_index()
        
        logger.info("年代趋势分析完成")
        return decade_counts
    
    def country_distribution(self, top_n: int = 10) -> pd.Series:
        """
        国家/地区分布分析
        
        Args:
            top_n: 返回前N个国家
        
        Returns:
            国家分布计数
        """
        # 过滤空值
        valid_countries = self.df[self.df['country'] != '']['country']
        
        # 统计分布
        country_counts = valid_countries.value_counts().head(top_n)
        
        logger.info(f"国家分布分析完成（Top {top_n}）")
        return country_counts
    
    def director_analysis(self, top_n: int = 10) -> pd.DataFrame:
        """
        导演作品分析
        
        Args:
            top_n: 返回前N位导演
        
        Returns:
            导演分析DataFrame
        """
        # 过滤空值
        valid_directors = self.df[self.df['director'] != '']
        
        if len(valid_directors) == 0:
            logger.warning("没有有效的导演数据")
            return pd.DataFrame()
        
        # 统计每位导演的作品数量和平均评分
        director_stats = valid_directors.groupby('director').agg(
            movie_count=('title', 'count'),
            avg_rating=('rating', 'mean'),
            total_votes=('rating_people', 'sum')
        ).reset_index()
        
        # 按作品数量排序
        director_stats = director_stats.sort_values('movie_count', ascending=False).head(top_n)
        
        logger.info(f"导演分析完成（Top {top_n}）")
        return director_stats
    
    def generate_full_report(self) -> str:
        """
        生成完整分析报告
        
        Returns:
            报告文本
        """
        report = []
        report.append("=" * 60)
        report.append("豆瓣Top 250电影数据分析报告")
        report.append("=" * 60)
        report.append("")
        
        # 基础统计
        stats = self.basic_statistics()
        report.append("【基础统计】")
        report.append(f"总电影数: {stats['total_movies']}")
        report.append(f"平均评分: {stats['avg_rating']:.2f}")
        report.append(f"中位数评分: {stats['median_rating']:.2f}")
        report.append(f"最高评分: {stats['max_rating']}")
        report.append(f"最低评分: {stats['min_rating']}")
        report.append(f"评分标准差: {stats['std_rating']:.2f}")
        report.append(f"总评价人数: {stats['total_votes']:,}")
        report.append(f"平均评价人数: {stats['avg_votes']:,.0f}")
        report.append("")
        
        # 评分分布
        report.append("【评分分布】")
        rating_dist = self.rating_distribution()
        for bracket, count in rating_dist.items():
            bar = "█" * int(count / 5)
            report.append(f"  {bracket:>8}: {count:>3} 部 {bar}")
        report.append("")
        
        # 年代趋势
        report.append("【年代趋势（Top 10）】")
        year_trend = self.year_trend()
        for decade, count in year_trend.head(10).items():
            bar = "█" * int(count / 3)
            report.append(f"  {decade}s: {count:>3} 部 {bar}")
        report.append("")
        
        # 国家分布
        report.append("【国家/地区分布（Top 10）】")
        country_dist = self.country_distribution(10)
        for country, count in country_dist.items():
            bar = "█" * int(count / 3)
            report.append(f"  {country:>10}: {count:>3} 部 {bar}")
        report.append("")
        
        # 导演分析
        report.append("【最多作品导演（Top 10）】")
        director_df = self.director_analysis(10)
        if not director_df.empty:
            for _, row in director_df.iterrows():
                report.append(f"  {row['director']:20s}: {row['movie_count']:2d} 部, 均分 {row['avg_rating']:.2f}")
        report.append("")
        
        report_text = "\n".join(report)
        logger.info("完整报告生成完成")
        
        return report_text
