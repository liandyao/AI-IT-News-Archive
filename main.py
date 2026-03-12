import datetime
import os
from news_scraper import fetch_all_news
from qwen_llm import summarize_news_with_qwen, analyze_news_with_qwen
from git_utils import push_to_github, clone_github_repo

def generate_daily_summary(summarized_news):
    """
    生成每日新闻总结
    """
    # 分类新闻
    ai_news = [news for news in summarized_news if 'AI' in news['summary'] or '人工智能' in news['summary']]
    tech_news = [news for news in summarized_news if '科技' in news['summary'] or 'IT' in news['summary']]
    other_news = [news for news in summarized_news if news not in ai_news and news not in tech_news]
    
    # 生成总结
    summary = f"# 每日IT和AI新闻总结\n\n"
    summary += f"## 概览\n"
    summary += f"今日共收集到 {len(summarized_news)} 条新闻，其中AI相关新闻 {len(ai_news)} 条，科技相关新闻 {len(tech_news)} 条。\n\n"
    
    if ai_news:
        summary += f"## AI新闻\n"
        for i, news in enumerate(ai_news, 1):
            summary += f"### {i}. {news['title']}\n"
            summary += f"**来源:** {news['source']}\n"
            summary += f"**摘要:** {news['summary']}\n"
            summary += f"**链接:** {news['link']}\n\n"
    
    if tech_news:
        summary += f"## 科技新闻\n"
        for i, news in enumerate(tech_news, 1):
            summary += f"### {i}. {news['title']}\n"
            summary += f"**来源:** {news['source']}\n"
            summary += f"**摘要:** {news['summary']}\n"
            summary += f"**链接:** {news['link']}\n\n"
    
    if other_news:
        summary += f"## 其他新闻\n"
        for i, news in enumerate(other_news, 1):
            summary += f"### {i}. {news['title']}\n"
            summary += f"**来源:** {news['source']}\n"
            summary += f"**摘要:** {news['summary']}\n"
            summary += f"**链接:** {news['link']}\n\n"
    
    return summary

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
    api_key = os.environ.get('QWEN_API_KEY')
    summarized_news = summarize_news_with_qwen(news, api_key)
    
    # 生成每日总结
    daily_summary = generate_daily_summary(summarized_news)
    
    # 保存为markdown文件
    output_dir = os.path.join(os.getcwd(), 'news_archives')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'{today}_news_summary.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(daily_summary)
    
    # 分析新闻趋势（使用Qwen LLM）
    print("\n开始分析新闻趋势...")
    trend_analysis = analyze_news_with_qwen(summarized_news, api_key)
    
    # 生成趋势报告
    trend_report = f"# 每日IT和AI新闻趋势分析\n\n{trend_analysis}"
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