from typing import List, Dict

def summarize_news(news_items: List[Dict]) -> List[Dict]:
    """
    总结新闻内容
    基于规则的总结方法
    """
    summarized_news = []
    
    for news in news_items:
        title = news.get('title', '')
        source = news.get('source', '')
        link = news.get('link', '')
        
        # 基于标题生成摘要
        summary = generate_summary_from_title(title, source)
        
        summarized_news.append({
            'title': title,
            'link': link,
            'source': source,
            'summary': summary
        })
    
    return summarized_news

def generate_summary_from_title(title: str, source: str) -> str:
    """
    基于标题生成新闻摘要
    """
    # 关键词匹配
    ai_keywords = ['AI', '人工智能', '机器学习', '深度学习', '大模型', '智能', '算法']
    tech_keywords = ['科技', 'IT', '互联网', '手机', '电脑', '软件', '硬件', '技术']
    
    has_ai_keyword = any(keyword in title for keyword in ai_keywords)
    has_tech_keyword = any(keyword in title for keyword in tech_keywords)
    
    if has_ai_keyword:
        return f"这是一条关于人工智能技术的新闻，来自{source}。新闻标题涉及{extract_keywords(title)}等内容，可能包含最新的AI技术发展或应用。"
    elif has_tech_keyword:
        return f"这是一条科技新闻，来自{source}。新闻标题涉及{extract_keywords(title)}等内容，可能包含最新的科技产品发布或技术发展。"
    else:
        return f"这是一条来自{source}的新闻，标题为{title}，可能包含相关领域的最新动态。"

def extract_keywords(text: str) -> str:
    """
    从文本中提取关键词
    """
    # 简单的关键词提取
    keywords = []
    
    # 常见技术关键词
    tech_terms = ['AI', '人工智能', '机器学习', '深度学习', '大模型', '科技', 'IT', '互联网', '手机', '电脑', '软件', '硬件', '技术']
    
    for term in tech_terms:
        if term in text:
            keywords.append(term)
    
    if keywords:
        return '、'.join(keywords)
    else:
        # 提取标题中的名词性短语
        words = text.split()
        important_words = [word for word in words if len(word) > 2]
        return '、'.join(important_words[:3])

def generate_daily_summary(summarized_news: List[Dict]) -> str:
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