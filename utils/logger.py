"""
日志系统模块 - 提供结构化的日志记录功能
"""

import logging
import sys
from pathlib import Path
from config import LogConfig


def setup_logger(name: str = "douban_scraper", log_file: Path = None) -> logging.Logger:
    """
    配置并返回logger实例
    
    Args:
        name: logger名称
        log_file: 日志文件路径，默认为配置中的路径
    
    Returns:
        配置好的logger实例
    """
    if log_file is None:
        log_file = LogConfig.LOG_FILE
    
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LogConfig.LOG_LEVEL))
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        fmt=LogConfig.LOG_FORMAT,
        datefmt=LogConfig.DATE_FORMAT
    )
    
    # 控制台Handler（彩色输出）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件Handler
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"无法创建日志文件: {e}")
    
    return logger


# 创建默认logger实例
logger = setup_logger()
