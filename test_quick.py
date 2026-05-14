"""
快速测试脚本 - 验证项目基本功能
===============================
不实际爬取数据，仅测试模块导入和基础功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """测试所有模块是否可以正常导入"""
    print("测试模块导入...")
    
    try:
        import config
        print("✓ config 模块导入成功")
        
        from utils.logger import setup_logger
        print("✓ utils.logger 模块导入成功")
        
        from utils.helpers import safe_get, format_number, extract_year
        print("✓ utils.helpers 模块导入成功")
        
        from scraper.data_parser import MovieParser
        print("✓ scraper.data_parser 模块导入成功")
        
        from scraper.anti_crawl import AntiCrawlStrategy
        print("✓ scraper.anti_crawl 模块导入成功")
        
        from storage.csv_storage import CSVStorage
        print("✓ storage.csv_storage 模块导入成功")
        
        from storage.json_storage import JSONStorage
        print("✓ storage.json_storage 模块导入成功")
        
        from analyzer.data_cleaner import DataCleaner
        print("✓ analyzer.data_cleaner 模块导入成功")
        
        from analyzer.statistical_analysis import StatisticalAnalyzer
        print("✓ analyzer.statistical_analysis 模块导入成功")
        
        from analyzer.visualizer import DataVisualizer
        print("✓ analyzer.visualizer 模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_helpers():
    """测试辅助函数"""
    print("\n测试辅助函数...")
    
    from utils.helpers import safe_get, format_number, extract_year
    
    # 测试 safe_get
    data = {'name': 'test', 'value': 123}
    assert safe_get(data, 'name') == 'test'
    assert safe_get(data, 'missing', 'default') == 'default'
    print("✓ safe_get 函数正常")
    
    # 测试 format_number
    assert format_number("2494028人评价") == 2494028
    assert format_number("") == 0
    print("✓ format_number 函数正常")
    
    # 测试 extract_year
    assert extract_year("1994") == "1994"
    assert extract_year("1994年") == "1994"
    print("✓ extract_year 函数正常")
    
    return True


def test_config():
    """测试配置加载"""
    print("\n测试配置加载...")
    
    from config import ScraperConfig, ProxyConfig, AnalysisConfig
    
    assert ScraperConfig.TOTAL_PAGES == 10
    assert ScraperConfig.MOVIES_PER_PAGE == 25
    print("✓ ScraperConfig 配置正确")
    
    assert isinstance(ProxyConfig.ENABLE_PROXY, bool)
    print("✓ ProxyConfig 配置正确")
    
    assert AnalysisConfig.DPI == 300
    print("✓ AnalysisConfig 配置正确")
    
    return True


def main():
    """运行所有测试"""
    print("=" * 60)
    print("豆瓣Top 250高级爬虫项目 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("辅助函数", test_helpers),
        ("配置加载", test_config),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} 测试异常: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")
    
    all_passed = all(r for _, r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！项目可以正常使用。")
    else:
        print("❌ 部分测试失败，请检查错误信息。")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
