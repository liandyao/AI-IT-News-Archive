# AI-IT-News-Archive

一个自动化的IT和AI新闻收集、摘要分析和归档系统，通过RSS订阅获取最新新闻，使用大语言模型生成摘要，并自动推送到GitHub仓库进行历史记录管理。

## 功能特点

- **RSS新闻采集**: 从多个IT和AI相关网站获取最新新闻
  - IT之家
  - 36氪 
  - 少数派

- **智能摘要**: 使用Qwen3-30B-A3B大语言模型生成新闻摘要
  - 自动提取新闻核心内容
  - 直接使用大模型生成，不使用降级机制

- **趋势分析**: 分析每日新闻关键词和趋势
  - 关键词提取
  - 热点话题分析

- **自动化归档**: 自动将新闻摘要和趋势分析推送到GitHub
  - 每日新闻报告
  - 历史数据管理

## 系统要求

- Python 3.7+
- pip包管理器

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/liandyao/AI-IT-News-Archive.git
cd AI-IT-News-Archive
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

1. **API密钥配置**：
   - 推荐使用环境变量设置Qwen API密钥：
   ```bash
   # Windows
   set QWEN_API_KEY=your_qwen_api_key_here
   
   # Linux/Mac
   export QWEN_API_KEY=your_qwen_api_key_here
   ```
   - 或直接编辑 `main.py` 文件中的API密钥配置

2. **GitHub配置**：
   - 确保你有GitHub仓库的推送权限
   - 仓库URL在 `main.py` 中配置：
   ```python
   repo_url = "https://github.com/liandyao/AI-IT-News-Archive.git"
   ```

## 使用方法

### 手动运行

运行主程序获取今日新闻：
```bash
python main.py
```

### 自动化运行

使用 `auto_update.py` 设置定时任务：
```bash
python auto_update.py
```

## 项目结构

```
AI-IT-News-Archive/
├── main.py                 # 主程序入口
├── news_scraper.py         # RSS新闻采集模块
├── qwen_llm.py            # Qwen LLM API集成
├── git_utils.py           # Git工具函数
├── auto_update.py         # 自动更新脚本
├── test_llm.py            # LLM测试脚本
├── test_summary.py        # 摘要生成测试脚本
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明文档
├── .github/              # GitHub配置目录
│   └── workflows/        # GitHub Actions工作流
│       └── daily-update.yml  # 每日更新工作流
└── news_archives/        # 新闻归档目录
```

## 输出文件

程序运行后会生成以下文件：

1. **每日新闻摘要**: `YYYY-MM-DD_news_summary.md`
   - AI相关新闻
   - 科技新闻
   - 其他新闻

2. **趋势分析报告**: `YYYY-MM-DD_trend_analysis.md`
   - 关键词统计
   - 热点话题分析

## 依赖包

- `requests`: HTTP请求
- `feedparser`: RSS解析
- `openai`: OpenAI API客户端

## 注意事项

1. **API限制**: Qwen API有调用频率限制，建议合理安排调用频率
2. **网络环境**: 确保网络连接正常，能够访问RSS源和API服务
3. **GitHub权限**: 确保有GitHub仓库的推送权限
4. **API密钥安全**: 建议使用环境变量存储API密钥，避免硬编码在代码中

## 故障排除

### API调用失败
- 检查API密钥是否正确
- 检查网络连接
- 查看API配额是否用尽

### RSS获取失败
- 检查网络连接
- 确认RSS源URL是否有效
- 查看防火墙设置

### GitHub推送失败
- 检查仓库URL是否正确
- 确认有推送权限
- 检查Git配置

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- GitHub: https://github.com/liandyao/AI-IT-News-Archive
