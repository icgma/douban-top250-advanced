"""
豆瓣Top 250高级爬虫项目 - 主入口
=================================
集成爬虫、存储、分析全流程
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scraper.async_scraper import run_scraper
from storage.csv_storage import CSVStorage
from storage.json_storage import JSONStorage
from analyzer.data_cleaner import DataCleaner
from analyzer.statistical_analysis import StatisticalAnalyzer
from analyzer.visualizer import DataVisualizer
from utils.logger import logger


async def main():
    """
    主函数 - 执行完整流程
    
    流程：
    1. 爬取数据
    2. 存储数据（CSV + JSON）
    3. 数据清洗
    4. 统计分析
    5. 生成可视化图表
    """
    logger.info("=" * 60)
    logger.info("豆瓣Top 250高级爬虫项目启动")
    logger.info("=" * 60)
    
    try:
        # Step 1: 爬取数据
        logger.info("\n【Step 1】开始爬取数据...")
        movies = await run_scraper()
        
        if not movies:
            logger.error("爬取失败，没有获取到数据")
            return
        
        logger.info(f"成功爬取 {len(movies)} 部电影\n")
        
        # Step 2: 存储数据
        logger.info("【Step 2】开始存储数据...")
        csv_storage = CSVStorage()
        csv_storage.save(movies)
        
        json_storage = JSONStorage()
        json_storage.save(movies)
        logger.info("数据存储完成\n")
        
        # Step 3: 数据清洗
        logger.info("【Step 3】开始数据清洗...")
        cleaner = DataCleaner(movies)
        df_cleaned = cleaner.clean()
        logger.info(f"数据清洗完成，剩余 {len(df_cleaned)} 条记录\n")
        
        # Step 4: 统计分析
        logger.info("【Step 4】开始统计分析...")
        analyzer = StatisticalAnalyzer(df_cleaned)
        report = analyzer.generate_full_report()
        print("\n" + report)
        
        # 保存报告到文件
        report_file = Path("reports/summary.md")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"\n分析报告已保存: {report_file}\n")
        
        # Step 5: 生成可视化图表
        logger.info("【Step 5】开始生成可视化图表...")
        visualizer = DataVisualizer(df_cleaned)
        charts = visualizer.generate_all_charts()
        logger.info(f"共生成 {len(charts)} 个图表\n")
        
        logger.info("=" * 60)
        logger.info("✅ 全部流程完成！")
        logger.info("=" * 60)
        logger.info(f"数据文件:")
        logger.info(f"  - CSV: {csv_storage.filepath}")
        logger.info(f"  - JSON: {json_storage.filepath}")
        logger.info(f"  - 报告: {report_file}")
        logger.info(f"  - 图表: {visualizer.output_dir}")
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())
