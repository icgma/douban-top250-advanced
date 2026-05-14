# 快速开始指南

## 📦 安装步骤

### 1. 安装依赖包

```bash
pip install -r requirements.txt
```

如果安装速度慢，可以使用国内镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 验证安装

```bash
python test_quick.py
```

看到 "✅ 所有测试通过！" 即表示安装成功。

## 🚀 使用方法

### 方式一：完整流程（推荐）

一键执行爬取、存储、分析、可视化全流程：

```bash
python main.py
```

**执行过程：**
1. 爬取豆瓣Top 250全部10页数据（约需30-60秒）
2. 保存为CSV和JSON格式到 `data/` 目录
3. 执行数据清洗和验证
4. 生成统计分析报告到 `reports/summary.md`
5. 创建4个可视化图表到 `reports/charts/`

**输出文件：**
```
data/
├── douban_top250.csv          # CSV格式数据
├── douban_top250.json         # JSON格式数据
└── .checkpoint.json           # 断点续传记录

reports/
├── summary.md                 # 文本分析报告
└── charts/
    ├── rating_distribution.png    # 评分分布图
    ├── year_trend.png             # 年代趋势图
    ├── country_distribution.png   # 国家分布图
    └── dashboard.png              # 综合仪表板
```

### 方式二：仅数据分析

如果已有数据文件，可以单独运行分析：

```bash
python run_analysis.py
```

这会读取 `data/douban_top250.json` 并生成分析报告和图表。

## 📊 查看结果

### 1. 查看数据文件

**CSV文件**（可用Excel打开）：
```bash
# Windows
start data\douban_top250.csv

# macOS
open data/douban_top250.csv

# Linux
xdg-open data/douban_top250.csv
```

**JSON文件**（可用文本编辑器或浏览器打开）：
```bash
# Windows
notepad data\douban_top250.json

# macOS/Linux
cat data/douban_top250.json | head -50
```

### 2. 查看分析报告

```bash
# Windows
type reports\summary.md

# macOS/Linux
cat reports/summary.md
```

### 3. 查看可视化图表

```bash
# Windows - 打开图表文件夹
start reports\charts

# macOS
open reports/charts

# Linux
xdg-open reports/charts
```

双击任意 `.png` 文件即可查看图表。

## ⚙️ 自定义配置

如需调整爬虫参数，编辑 `config.py` 文件：

```python
# 调整并发数（默认3）
ScraperConfig.MAX_CONCURRENT_REQUESTS = 5

# 调整延迟时间（默认1-3秒）
ScraperConfig.MIN_DELAY = 0.5
ScraperConfig.MAX_DELAY = 2.0

# 调整重试次数（默认3次）
ScraperConfig.MAX_RETRIES = 5
```

⚠️ **注意**：过快的请求可能触发豆瓣的反爬机制。

## 🔄 断点续传

如果爬取过程中中断，直接重新运行即可：

```bash
python main.py
```

程序会自动从上次中断的位置继续爬取。

## 🐛 常见问题

### Q1: 提示缺少某个模块？

**A**: 重新安装依赖：
```bash
pip install -r requirements.txt
```

### Q2: 爬取速度很慢？

**A**: 这是正常现象，为了遵守爬虫伦理，程序设置了1-3秒的延迟。如需加速，可修改config.py中的延迟参数，但可能触发反爬。

### Q3: 遇到403错误？

**A**: 可能触发了豆瓣的反爬机制：
1. 等待一段时间后重试
2. 增加延迟时间
3. 启用代理（需配置ProxyConfig）

### Q4: 图表中文乱码？

**A**: 确保系统安装了中文字体：
- Windows: 通常已预装SimHei
- macOS: 使用Arial Unicode MS
- Linux: 安装wqy-zenhei字体
  ```bash
  sudo apt-get install fonts-wqy-zenhei
  ```

### Q5: 如何只爬取部分页面？

**A**: 修改 `config.py`：
```python
ScraperConfig.TOTAL_PAGES = 5  # 只爬取前5页（125部电影）
```

## 📚 学习资源

### 代码阅读顺序

建议按以下顺序阅读代码，理解项目架构：

1. **config.py** - 了解配置结构
2. **utils/helpers.py** - 理解辅助函数
3. **utils/logger.py** - 学习日志系统
4. **scraper/data_parser.py** - 学习HTML解析
5. **scraper/anti_crawl.py** - 学习反爬策略
6. **scraper/async_scraper.py** - 学习异步编程
7. **storage/*.py** - 学习数据存储
8. **analyzer/data_cleaner.py** - 学习数据清洗
9. **analyzer/statistical_analysis.py** - 学习统计分析
10. **analyzer/visualizer.py** - 学习数据可视化
11. **main.py** - 理解整体流程

### 扩展练习

1. **基础**: 修改代码，只爬取前50部电影
2. **中级**: 添加新的统计维度（如类型分布）
3. **高级**: 实现详情页爬取，获取更多信息
4. **挑战**: 构建Web界面展示数据

## 💡 教学建议

### 课堂演示

1. 先运行 `test_quick.py` 验证环境
2. 展示项目结构和模块划分
3. 逐步讲解核心代码（async_scraper.py, data_parser.py）
4. 运行 `main.py` 展示完整流程
5. 查看生成的数据和图表

### 学生作业

**作业1**: 理解爬虫原理
- 阅读 scraper/ 模块代码
- 画出爬取流程图
- 解释反爬策略的工作原理

**作业2**: 数据分析实践
- 修改 statistical_analysis.py，添加新的统计维度
- 生成额外的可视化图表
- 撰写简短的分析报告

**作业3**: 功能扩展
- 实现详情页爬取
- 添加情感分析功能
- 构建简单的Web展示页面

## 📞 技术支持

如遇到问题：

1. 查看 `logs/scraper.log` 日志文件
2. 检查 README.md 中的常见问题
3. 参考 PROJECT_SUMMARY.md 了解项目详情

---

**祝使用愉快！** 🎉
