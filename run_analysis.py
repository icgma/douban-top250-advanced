"""
独立分析脚本 - 对已有数据进行深度分析
========================================
使用方法：
  python run_analysis.py

前提条件：
  需要先运行爬虫获取数据（data/douban_top250.json）
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from analyzer.data_cleaner import DataCleaner
from analyzer.statistical_analysis import StatisticalAnalyzer
from analyzer.visualizer import DataVisualizer
from utils.logger import logger


def load_data(json_file: Path = None) -> list:
    """
    加载JSON数据文件
    
    Args:
        json_file: JSON文件路径
    
    Returns:
        电影数据列表
    """
    if json_file is None:
        json_file = Path("data/douban_top250.json")
    
    if not json_file.exists():
        logger.error(f"数据文件不存在: {json_file}")
        logger.info("请先运行 main.py 爬取数据")
        sys.exit(1)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        movies = json.load(f)
    
    logger.info(f"加载数据: {len(movies)} 部电影")
    return movies


def main():
    """
    主函数 - 执行数据分析流程
    """
    logger.info("=" * 60)
    logger.info("豆瓣Top 250数据分析启动")
    logger.info("=" * 60)
    
    try:
        # Step 1: 加载数据
        logger.info("\n【Step 1】加载数据...")
        movies = load_data()
        
        # Step 2: 数据清洗
        logger.info("【Step 2】数据清洗...")
        cleaner = DataCleaner(movies)
        df_cleaned = cleaner.clean()
        logger.info(f"清洗完成，剩余 {len(df_cleaned)} 条记录\n")
        
        # Step 3: 统计分析
        logger.info("【Step 3】统计分析...")
        analyzer = StatisticalAnalyzer(df_cleaned)
        report = analyzer.generate_full_report()
        print("\n" + report)
        
        # 保存报告
        report_file = Path("reports/analysis_report.md")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"\n报告已保存: {report_file}\n")
        
        # Step 4: 生成可视化
        logger.info("【Step 4】生成可视化图表...")
        visualizer = DataVisualizer(df_cleaned)
        charts = visualizer.generate_all_charts()
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ 分析完成！")
        logger.info("=" * 60)
        logger.info(f"输出文件:")
        logger.info(f"  - 报告: {report_file}")
        logger.info(f"  - 图表: {visualizer.output_dir}")
        
    except Exception as e:
        logger.error(f"分析过程出错: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
