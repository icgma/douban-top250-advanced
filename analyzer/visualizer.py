"""
数据可视化模块
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List
from config import AnalysisConfig
from utils.logger import logger

# 设置中文字体
plt.rcParams['font.sans-serif'] = AnalysisConfig.FONT_CONFIG['family']
plt.rcParams['axes.unicode_minus'] = False


class DataVisualizer:
    """
    数据可视化器
    
    功能：
    - 评分分布柱状图
    - 年代趋势折线图
    - 国家分布饼图
    - 综合仪表板
    """
    
    def __init__(self, df: pd.DataFrame, output_dir: Path = None):
        """
        初始化可视化器
        
        Args:
            df: 清洗后的电影数据DataFrame
            output_dir: 图表输出目录
        """
        self.df = df
        self.output_dir = output_dir or AnalysisConfig.CHARTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("数据可视化器初始化完成")
    
    def plot_rating_distribution(self) -> Path:
        """
        绘制评分分布柱状图
        
        Returns:
            保存的文件路径
        """
        fig, ax = plt.subplots(figsize=AnalysisConfig.FIGURE_SIZE)
        
        # 定义评分段
        bins = [0, 8.0, 8.5, 9.0, 10]
        labels = ['<8.0', '8.0-8.4', '8.5-8.9', '9.0+']
        self.df['rating_bracket'] = pd.cut(self.df['rating'], bins=bins, labels=labels)
        
        distribution = self.df['rating_bracket'].value_counts().sort_index()
        
        # 绘制柱状图
        bars = ax.bar(distribution.index.astype(str), distribution.values, 
                      color=AnalysisConfig.COLOR_PALETTE['primary'],
                      edgecolor='white', linewidth=2)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_title('豆瓣Top 250电影评分分布', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('评分段', fontsize=12)
        ax.set_ylabel('电影数量', fontsize=12)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        filepath = self.output_dir / 'rating_distribution.png'
        plt.savefig(filepath, dpi=AnalysisConfig.DPI, bbox_inches='tight')
        plt.close()
        
        logger.info(f"评分分布图已保存: {filepath}")
        return filepath
    
    def plot_year_trend(self) -> Path:
        """
        绘制年代趋势折线图
        
        Returns:
            保存的文件路径
        """
        # 提取有效年份
        valid_years = self.df[self.df['year'] != '']['year']
        valid_years = pd.to_numeric(valid_years, errors='coerce').dropna()
        
        # 按年代分组
        decades = (valid_years // 10 * 10).astype(int)
        decade_counts = decades.value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=AnalysisConfig.FIGURE_SIZE)
        
        # 绘制折线图
        ax.plot(decade_counts.index.astype(str), decade_counts.values, 
               marker='o', linewidth=2, markersize=8,
               color=AnalysisConfig.COLOR_PALETTE['secondary'])
        
        # 填充区域
        ax.fill_between(range(len(decade_counts)), decade_counts.values, 
                       alpha=0.2, color=AnalysisConfig.COLOR_PALETTE['secondary'])
        
        ax.set_title('豆瓣Top 250电影年代分布趋势', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('年代', fontsize=12)
        ax.set_ylabel('电影数量', fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filepath = self.output_dir / 'year_trend.png'
        plt.savefig(filepath, dpi=AnalysisConfig.DPI, bbox_inches='tight')
        plt.close()
        
        logger.info(f"年代趋势图已保存: {filepath}")
        return filepath
    
    def plot_country_distribution(self, top_n: int = 10) -> Path:
        """
        绘制国家/地区分布环形图
        
        Args:
            top_n: 显示前N个国家
        
        Returns:
            保存的文件路径
        """
        # 获取Top N国家
        valid_countries = self.df[self.df['country'] != '']['country']
        country_counts = valid_countries.value_counts().head(top_n)
        
        fig, ax = plt.subplots(figsize=AnalysisConfig.FIGURE_SIZE)
        
        # 绘制环形图
        wedges, texts, autotexts = ax.pie(
            country_counts.values,
            labels=country_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3.colors,
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
        )
        
        # 美化标签
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title(f'豆瓣Top 250电影国家/地区分布（Top {top_n}）', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        filepath = self.output_dir / 'country_distribution.png'
        plt.savefig(filepath, dpi=AnalysisConfig.DPI, bbox_inches='tight')
        plt.close()
        
        logger.info(f"国家分布图已保存: {filepath}")
        return filepath
    
    def create_dashboard(self) -> Path:
        """
        创建综合分析仪表板
        
        Returns:
            保存的文件路径
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('豆瓣Top 250电影综合数据分析仪表板', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        # 1. 评分分布
        bins = [0, 8.0, 8.5, 9.0, 10]
        labels = ['<8.0', '8.0-8.4', '8.5-8.9', '9.0+']
        self.df['rating_bracket'] = pd.cut(self.df['rating'], bins=bins, labels=labels)
        rating_dist = self.df['rating_bracket'].value_counts().sort_index()
        
        axes[0, 0].bar(rating_dist.index.astype(str), rating_dist.values,
                      color=AnalysisConfig.COLOR_PALETTE['primary'],
                      edgecolor='white', linewidth=2)
        axes[0, 0].set_title('评分分布', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('评分段')
        axes[0, 0].set_ylabel('电影数量')
        axes[0, 0].grid(axis='y', alpha=0.3, linestyle='--')
        
        # 2. 年代趋势
        valid_years = self.df[self.df['year'] != '']['year']
        valid_years = pd.to_numeric(valid_years, errors='coerce').dropna()
        decades = (valid_years // 10 * 10).astype(int)
        decade_counts = decades.value_counts().sort_index()
        
        axes[0, 1].plot(decade_counts.index.astype(str), decade_counts.values,
                       marker='o', linewidth=2, markersize=6,
                       color=AnalysisConfig.COLOR_PALETTE['secondary'])
        axes[0, 1].set_title('年代趋势', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('年代')
        axes[0, 1].set_ylabel('电影数量')
        axes[0, 1].grid(True, alpha=0.3, linestyle='--')
        plt.setp(axes[0, 1].xaxis.get_majorticklabels(), rotation=45)
        
        # 3. 国家分布（Top 8）
        valid_countries = self.df[self.df['country'] != '']['country']
        country_counts = valid_countries.value_counts().head(8)
        
        axes[1, 0].barh(range(len(country_counts)), country_counts.values,
                       color=AnalysisConfig.COLOR_PALETTE['accent'])
        axes[1, 0].set_yticks(range(len(country_counts)))
        axes[1, 0].set_yticklabels(country_counts.index)
        axes[1, 0].set_title('国家/地区分布（Top 8）', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('电影数量')
        axes[1, 0].invert_yaxis()
        axes[1, 0].grid(axis='x', alpha=0.3, linestyle='--')
        
        # 4. 评分与评价人数散点图
        scatter = axes[1, 1].scatter(self.df['rating'], self.df['rating_people'],
                                    c=self.df['rating'], cmap='viridis',
                                    alpha=0.6, edgecolors='white', linewidth=0.5)
        axes[1, 1].set_title('评分 vs 评价人数', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('评分')
        axes[1, 1].set_ylabel('评价人数')
        axes[1, 1].grid(True, alpha=0.3, linestyle='--')
        plt.colorbar(scatter, ax=axes[1, 1])
        
        plt.tight_layout()
        
        filepath = self.output_dir / 'dashboard.png'
        plt.savefig(filepath, dpi=AnalysisConfig.DPI, bbox_inches='tight')
        plt.close()
        
        logger.info(f"综合仪表板已保存: {filepath}")
        return filepath
    
    def generate_all_charts(self) -> List[Path]:
        """
        生成所有图表
        
        Returns:
            生成的文件路径列表
        """
        logger.info("开始生成所有图表...")
        
        charts = []
        charts.append(self.plot_rating_distribution())
        charts.append(self.plot_year_trend())
        charts.append(self.plot_country_distribution())
        charts.append(self.create_dashboard())
        
        logger.info(f"共生成 {len(charts)} 个图表")
        return charts
