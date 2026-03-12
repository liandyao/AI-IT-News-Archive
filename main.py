import datetime
import os
from news_scraper import fetch_all_news
from llm_summarizer import summarize_news, generate_daily_summary
from qwen_llm import summarize_news_with_qwen
from git_utils import push_to_github, clone_github_repo
from news_analyzer import analyze_news_trends, generate_trend_report

def main():
    """主函数"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"开始处理{today}的IT和AI新闻...")
    
    # 获取新闻
    news = fetch_all_news()
    
    if not news:
        print("没有获取到新闻，程序退出")
        return
    
    # 总结新闻（使用Qwen LLM）
    api_key = "sk-MjczLTExMTc0MTY2NjIzLTE3NzMzMTY2NjQ2MjU="  # 替换为真实的API密钥
    if api_key and api_key != "your_qwen_api_key_here":
        summarized_news = summarize_news_with_qwen(news, api_key)
    else:
        # 降级到基于规则的摘要
        summarized_news = summarize_news(news)
    
    # 生成每日总结
    daily_summary = generate_daily_summary(summarized_news)
    
    # 保存为markdown文件
    output_dir = os.path.join(os.getcwd(), 'news_archives')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'{today}_news_summary.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(daily_summary)
    
    # 分析新闻趋势
    print("\n开始分析新闻趋势...")
    trend_analysis = analyze_news_trends(summarized_news)
    
    # 生成趋势报告
    trend_report = generate_trend_report(trend_analysis)
    trend_file = os.path.join(output_dir, f'{today}_trend_analysis.md')
    with open(trend_file, 'w', encoding='utf-8') as f:
        f.write(trend_report)
    
    # 推送文件到GitHub
    print("\n开始推送文件到GitHub...")
    repo_url = "https://github.com/liandyao/AI-IT-News-Archive.git"
    local_repo = os.path.join(os.getcwd(), "github_repo")
    
    # 克隆仓库
    if clone_github_repo(repo_url, local_repo):
        # 推送新闻摘要
        push_to_github(output_file, local_repo)
        # 推送趋势分析
        push_to_github(trend_file, local_repo)
    
    print(f"\n新闻总结已保存到: {output_file}")
    print(f"趋势分析已保存到: {trend_file}")
    print(f"共处理了{len(news)}条新闻")

if __name__ == "__main__":
    main()