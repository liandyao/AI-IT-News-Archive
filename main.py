import datetime
import os
from news_scraper import fetch_all_news

def generate_news_md(news_items):
    """
    生成新闻MD文件内容
    :param news_items: 新闻列表
    :return: MD格式的新闻内容
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    md_content = f"# 每日IT和AI新闻\n\n"
    md_content += f"## 概览\n"
    md_content += f"日期: {today}\n"
    md_content += f"共收集到 {len(news_items)} 条新闻\n\n"
    
    # 按来源分类
    news_by_source = {}
    for news in news_items:
        source = news.get('source', '未知来源')
        if source not in news_by_source:
            news_by_source[source] = []
        news_by_source[source].append(news)
    
    # 按来源输出新闻
    for source, source_news in news_by_source.items():
        md_content += f"## {source}\n"
        for i, news in enumerate(source_news, 1):
            title = news.get('title', '无标题')
            link = news.get('link', '')
            pub_date = news.get('date', '未知时间')
            description = news.get('description', '无内容')
            
            md_content += f"### {i}. {title}\n"
            md_content += f"**发布时间:** {pub_date}\n"
            md_content += f"**链接:** [{link}]({link})\n"
            if description:
                md_content += f"**正文:** {description}\n"
            md_content += "\n"
    
    return md_content

def save_news_to_md(news_items):
    """
    保存新闻到MD文件
    :param news_items: 新闻列表
    :return: 保存的文件路径
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join(os.getcwd(), 'news_archives')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'{today}_news.md')
    md_content = generate_news_md(news_items)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_file

def main():
    """
    主函数：获取新闻并保存到MD文件
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"开始处理{today}的IT和AI新闻...")
    
    # 获取新闻
    news = fetch_all_news()
    
    if not news:
        print("没有获取到新闻，程序退出")
        return
    
    # 保存新闻到MD文件
    output_file = save_news_to_md(news)
    
    print(f"\n新闻已保存到: {output_file}")
    print(f"共处理了{len(news)}条新闻")

if __name__ == "__main__":
    main()