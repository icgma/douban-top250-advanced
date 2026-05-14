"""
辅助函数模块 - 提供通用工具函数
"""

import re
from typing import Optional, Any


def safe_get(data: dict, key: str, default: Any = "") -> Any:
    """
    安全地从字典中获取值，避免KeyError
    
    Args:
        data: 字典数据
        key: 键名
        default: 默认值
    
    Returns:
        对应的值或默认值
    """
    return data.get(key, default) if data else default


def format_number(num_str: str) -> int:
    """
    格式化数字字符串，提取纯数字
    
    Args:
        num_str: 包含数字的字符串，如 "2494028人评价"
    
    Returns:
        提取的整数
    """
    if not num_str:
        return 0
    
    match = re.search(r'(\d+)', str(num_str))
    return int(match.group(1)) if match else 0


def extract_year(year_str: str) -> str:
    """
    从年份字符串中提取纯数字年份
    
    Args:
        year_str: 年份字符串，如 "1994" 或 "1994年"
    
    Returns:
        纯数字年份字符串
    """
    if not year_str:
        return ""
    
    match = re.search(r'(\d{4})', str(year_str))
    return match.group(1) if match else year_str.strip()


def validate_movie_data(movie: dict) -> bool:
    """
    验证电影数据的完整性
    
    Args:
        movie: 电影数据字典
    
    Returns:
        数据是否有效
    """
    required_fields = ['rank', 'title', 'rating']
    
    # 检查必需字段是否存在
    for field in required_fields:
        if field not in movie or not movie[field]:
            return False
    
    # 检查排名是否为有效数字
    if not isinstance(movie['rank'], (int, float)):
        return False
    
    # 检查评分是否在合理范围内
    try:
        rating = float(movie['rating'])
        if rating < 0 or rating > 10:
            return False
    except (ValueError, TypeError):
        return False
    
    return True


def calculate_progress(current: int, total: int, width: int = 50) -> str:
    """
    计算并生成进度条字符串
    
    Args:
        current: 当前进度
        total: 总数
        width: 进度条宽度
    
    Returns:
        进度条字符串
    """
    percentage = current / total * 100 if total > 0 else 0
    filled = int(width * current / total) if total > 0 else 0
    bar = '█' * filled + '-' * (width - filled)
    return f'|{bar}| {percentage:.1f}% ({current}/{total})'


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
    
    Returns:
        清理后的文件名
    """
    # 移除Windows文件系统不允许的字符
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # 限制长度
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename.strip()
