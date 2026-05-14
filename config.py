"""
配置文件 - 豆瓣Top250高级爬虫项目
=================================
集中管理所有配置参数，便于维护和调整
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# ============================================================
# 爬虫配置
# ============================================================
class ScraperConfig:
    # 豆瓣Top250基础URL
    BASE_URL = "https://movie.douban.com/top250"
    
    # 请求头配置
    DEFAULT_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # 爬取参数
    TOTAL_PAGES = 10  # 总页数（每页25部电影）
    MOVIES_PER_PAGE = 25
    TOTAL_MOVIES = TOTAL_PAGES * MOVIES_PER_PAGE  # 250部
    
    # 并发控制
    MAX_CONCURRENT_REQUESTS = 3  # 最大并发请求数
    REQUEST_TIMEOUT = 10  # 请求超时时间（秒）
    
    # 延迟控制（秒）
    MIN_DELAY = 1.0  # 最小延迟
    MAX_DELAY = 3.0  # 最大延迟
    DELAY_BETWEEN_PAGES = 2.0  # 页面间固定延迟
    
    # 重试配置
    MAX_RETRIES = 3  # 最大重试次数
    RETRY_DELAY = 5  # 重试间隔（秒）
    
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 存储文件路径
    CSV_FILE = OUTPUT_DIR / "douban_top250.csv"
    JSON_FILE = OUTPUT_DIR / "douban_top250.json"
    SQLITE_DB = OUTPUT_DIR / "douban_top250.db"
    
    # 断点续传记录文件
    CHECKPOINT_FILE = OUTPUT_DIR / ".checkpoint.json"


# ============================================================
# 代理池配置
# ============================================================
class ProxyConfig:
    ENABLE_PROXY = False  # 是否启用代理（默认关闭，按需开启）
    
    # 免费代理源（示例，实际使用时需要替换为有效的代理源）
    PROXY_SOURCES = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    ]
    
    # 代理测试URL
    TEST_URL = "https://httpbin.org/ip"
    
    # 代理有效期（秒）
    PROXY_TIMEOUT = 300  # 5分钟
    
    # 最大代理池大小
    MAX_POOL_SIZE = 50


# ============================================================
# 数据分析配置
# ============================================================
class AnalysisConfig:
    # 图表输出目录
    CHARTS_DIR = PROJECT_ROOT / "reports" / "charts"
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 图表配置
    FIGURE_SIZE = (12, 8)  # 默认图表尺寸
    DPI = 300  # 图像分辨率
    
    # 颜色主题
    COLOR_PALETTE = {
        'primary': '#2E86AB',
        'secondary': '#A23B72',
        'accent': '#F18F01',
        'success': '#C73E1D',
    }
    
    # 字体配置（支持中文）
    FONT_CONFIG = {
        'family': ['SimHei', 'Microsoft YaHei', 'DejaVu Sans'],
        'size': 12,
    }


# ============================================================
# 日志配置
# ============================================================
class LogConfig:
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_DIR.mkdir(exist_ok=True)
    
    LOG_FILE = LOG_DIR / "scraper.log"
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # 日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# 数据库配置（可选）
# ============================================================
class DatabaseConfig:
    # SQLite数据库连接字符串
    SQLITE_URI = f"sqlite:///{ScraperConfig.SQLITE_DB}"
    
    # 表名
    TABLE_NAME = "movies"
    
    # 是否启用数据库存储
    ENABLE_DATABASE = False
