# 🎬 豆瓣电影 Top250 高级爬虫项目

> Week11-12 进阶教学示范项目 - 异步爬虫 + 数据分析 + 可视化  
> 汕头大学 · 长江新闻与传播学院

## 📋 项目简介

本项目是一个**高级豆瓣电影Top 250爬虫系统**，相比基础版本增加了以下特性：

### ✨ 核心特性

- **异步并发爬取**: 使用aiohttp实现高效并发请求，提升爬取速度
- **智能反爬策略**: User-Agent轮换、智能延迟控制、请求头伪装
- **断点续传**: 支持中断后从上次位置继续爬取
- **多格式存储**: CSV、JSON双格式输出
- **数据清洗**: pandas数据清洗、去重、异常值处理
- **深度分析**: 评分分布、年代趋势、国家地区统计、导演作品分析
- **可视化报告**: 自动生成多维度图表和综合分析仪表板
- **教学友好**: 代码注释详细，模块化设计，适合教学演示

## 📁 项目结构

```
douban-top250-advanced/
├── README.md                    # 项目说明文档
├── requirements.txt             # 依赖包列表
├── config.py                    # 配置文件
├── main.py                      # 主入口（完整流程）
├── run_analysis.py              # 独立分析脚本
├── scraper/                     # 爬虫核心模块
│   ├── __init__.py
│   ├── async_scraper.py         # 异步爬虫主逻辑
│   ├── anti_crawl.py            # 反爬策略
│   └── data_parser.py           # 数据解析器
├── storage/                     # 数据存储模块
│   ├── __init__.py
│   ├── csv_storage.py           # CSV存储
│   └── json_storage.py          # JSON存储
├── analyzer/                    # 数据分析模块
│   ├── __init__.py
│   ├── data_cleaner.py          # 数据清洗
│   ├── statistical_analysis.py  # 统计分析
│   └── visualizer.py            # 可视化生成
├── utils/                       # 工具函数
│   ├── __init__.py
│   ├── logger.py                # 日志系统
│   └── helpers.py               # 辅助函数
├── data/                        # 数据输出目录（自动生成）
│   ├── douban_top250.csv
│   ├── douban_top250.json
│   └── .checkpoint.json         # 断点续传记录
├── reports/                     # 分析报告目录
│   ├── charts/                  # 图表文件
│   │   ├── rating_distribution.png
│   │   ├── year_trend.png
│   │   ├── country_distribution.png
│   │   └── dashboard.png
│   └── summary.md               # 分析总结
└── logs/                        # 日志目录（自动生成）
    └── scraper.log
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆或下载项目
cd douban-top250-advanced

# 安装依赖
pip install -r requirements.txt
```

**主要依赖：**
- aiohttp >= 3.8.0 (异步HTTP客户端)
- beautifulsoup4 >= 4.12.0 (HTML解析)
- pandas >= 2.0.0 (数据分析)
- matplotlib >= 3.7.0 (数据可视化)
- fake-useragent >= 1.1.0 (User-Agent轮换)
- tqdm >= 4.65.0 (进度条显示)

### 2. 运行完整流程

```bash
# 一键执行：爬取 → 存储 → 分析 → 可视化
python main.py
```

程序将自动：
1. 爬取豆瓣Top 250全部10页数据
2. 保存为CSV和JSON格式
3. 执行数据清洗和验证
4. 生成统计分析报告
5. 创建可视化图表

### 3. 仅运行数据分析

如果已有数据文件（`data/douban_top250.json`），可单独运行分析：

```bash
python run_analysis.py
```

## 📊 输出示例

### 数据统计卡片

```
【基础统计】
总电影数: 250
平均评分: 8.89
中位数评分: 8.90
最高评分: 9.7
最低评分: 8.0
总评价人数: 15,234,567
平均评价人数: 60,938
```

### 评分分布

```
【评分分布】
     <8.0:  12 部 ███
   8.0-8.4:  68 部 ██████████████
   8.5-8.9: 102 部 █████████████████████
     9.0+:  68 部 ██████████████
```

### 生成的图表

1. **评分分布柱状图** (`rating_distribution.png`)
2. **年代趋势折线图** (`year_trend.png`)
3. **国家分布环形图** (`country_distribution.png`)
4. **综合仪表板** (`dashboard.png`) - 包含4个子图

## 🎓 教学知识点

### 初级 (★☆☆)

- HTTP请求基础 (aiohttp异步请求)
- HTML解析 (BeautifulSoup选择器)
- 文件I/O (CSV/JSON写入)
- 异常处理 (try-except重试机制)

### 中级 (★★☆)

- 异步编程 (async/await模式)
- 并发控制 (TCPConnector限流)
- 数据清洗 (pandas数据处理)
- 模块化设计 (包结构和导入)

### 高级 (★★★)

- 反爬策略 (User-Agent轮换、智能延迟)
- 断点续传 (checkpoint机制)
- 统计分析 (分组聚合、分布计算)
- 数据可视化 (matplotlib/seaborn图表)
- 日志系统 (结构化日志记录)

## ⚙️ 配置说明

所有配置集中在 `config.py` 文件中：

```python
# 爬虫配置
ScraperConfig.MAX_CONCURRENT_REQUESTS = 3  # 并发数
ScraperConfig.MIN_DELAY = 1.0              # 最小延迟
ScraperConfig.MAX_DELAY = 3.0              # 最大延迟
ScraperConfig.MAX_RETRIES = 3              # 重试次数

# 代理配置（可选）
ProxyConfig.ENABLE_PROXY = False           # 是否启用代理

# 数据库配置（可选）
DatabaseConfig.ENABLE_DATABASE = False     # 是否启用SQLite
```

## 🛡️ 爬虫伦理

本项目遵循负责任的爬虫实践：

- ✅ 设置合理的User-Agent标识
- ✅ 控制请求频率（1-3秒间隔）
- ✅ 支持断点续传，避免重复请求
- ✅ 仅用于教学和研究目的
- ✅ 不涉及登录态和个人隐私数据
- ❌ 请勿大规模、高频率爬取
- ❌ 请勿用于商业用途

## 📚 知识衔接

| 周次 | 知识点 | 在本项目中的应用 |
|------|--------|-----------------|
| Week09 | 文件 I/O | CSV/JSON存储 |
| Week10 | pandas + Excel | 数据清洗与分析 |
| **Week11** | **requests + BeautifulSoup** | **爬虫基础** |
| **Week12** | **异步编程 + aiohttp** | **并发爬虫** |
| Week13 | 微信公众号数据 | 对比不同平台采集 |
| Week14 | 文本分析 | 短评情感分析扩展 |

## 🔧 扩展建议

### 功能扩展

1. **数据库存储**: 启用SQLite/MySQL持久化存储
2. **代理池**: 集成免费/付费代理服务
3. **详情页爬取**: 深入每部电影获取更多信息
4. **定时任务**: 使用APScheduler定期更新数据
5. **Web界面**: 使用Flask/FastAPI构建数据展示平台

### 分析扩展

1. **情感分析**: 对短评进行情感极性分析
2. **词云生成**: 基于短评生成词云图
3. **关联分析**: 导演-演员合作网络
4. **时间序列**: 评分随时间变化趋势
5. **推荐系统**: 基于协同过滤的电影推荐

## 🐛 常见问题

### Q1: 爬取速度慢？

**A:** 可以调整并发数和延迟：
```python
ScraperConfig.MAX_CONCURRENT_REQUESTS = 5  # 增加并发
ScraperConfig.MIN_DELAY = 0.5              # 减少延迟
```

⚠️ 注意：过快的请求可能触发反爬机制。

### Q2: 遇到403错误？

**A:** 可能触发了豆瓣的反爬机制：
- 增加延迟时间
- 启用代理池
- 暂停一段时间后重试

### Q3: 中文图表乱码？

**A:** 确保系统安装了中文字体：
- Windows: SimHei, Microsoft YaHei
- macOS: Arial Unicode MS
- Linux: 安装wqy-zenhei字体

### Q4: 如何恢复中断的爬取？

**A:** 项目支持自动断点续传，直接重新运行即可：
```bash
python main.py  # 自动从上次中断处继续
```

## 📝 许可证

本项目仅供教学使用，请遵守豆瓣网站的robots.txt和服务条款。

## 👥 贡献

欢迎提交Issue和Pull Request来改进项目！

---

**开发团队**: 汕头大学长江新闻与传播学院  
**课程**: 基础编程（Python基础与AI编程）  
**版本**: v1.0  
**更新日期**: 2026-05-15
