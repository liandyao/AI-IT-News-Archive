import re
from collections import Counter
from typing import List, Dict, Tuple
import jieba
import jieba.analyse

def extract_keywords(text: str, top_k: int = 10) -> List[Tuple[str, float]]:
    """
    提取文本中的关键词
    :param text: 文本内容
    :param top_k: 返回的关键词数量
    :return: 关键词列表，每个元素是(关键词, 权重)元组
    """
    try:
        # 使用jieba提取关键词
        keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
        return keywords
    except Exception as e:
        print(f"提取关键词时出错: {e}")
        return []

def analyze_news_trends(news_items: List[Dict]) -> Dict:
    """
    分析新闻趋势
    :param news_items: 新闻列表
    :return: 趋势分析结果
    """
    # 合并所有新闻标题和摘要
    all_text = " "
    for news in news_items:
        all_text += news.get('title', '') + " "
        all_text += news.get('summary', '') + " "
    
    # 提取关键词
    keywords = extract_keywords(all_text, top_k=20)
    
    # 统计来源分布
    source_counter = Counter()
    for news in news_items:
        source_counter[news.get('source', 'Unknown')] += 1
    
    # 分类统计
    ai_news = [news for news in news_items if 'AI' in news.get('summary', '') or '人工智能' in news.get('summary', '')]
    tech_news = [news for news in news_items if '科技' in news.get('summary', '') or 'IT' in news.get('summary', '')]
    other_news = [news for news in news_items if news not in ai_news and news not in tech_news]
    
    # 生成趋势报告
    trend_analysis = {
        'total_news': len(news_items),
        'ai_news_count': len(ai_news),
        'tech_news_count': len(tech_news),
        'other_news_count': len(other_news),
        'top_keywords': keywords,
        'source_distribution': dict(source_counter),
        'ai_news_percentage': (len(ai_news) / len(news_items) * 100) if news_items else 0,
        'tech_news_percentage': (len(tech_news) / len(news_items) * 100) if news_items else 0
    }
    
    return trend_analysis

def generate_trend_report(trend_analysis: Dict) -> str:
    """
    生成趋势分析报告
    :param trend_analysis: 趋势分析结果
    :return: 分析报告文本
    """
    report = f"# 新闻趋势分析报告\n\n"
    report += f"## 总体概览\n"
    report += f"- 总新闻数: {trend_analysis['total_news']}\n"
    report += f"- AI相关新闻: {trend_analysis['ai_news_count']} ({trend_analysis['ai_news_percentage']:.1f}%)\n"
    report += f"- 科技相关新闻: {trend_analysis['tech_news_count']} ({trend_analysis['tech_news_percentage']:.1f}%)\n"
    report += f"- 其他新闻: {trend_analysis['other_news_count']}\n\n"
    
    report += f"## 来源分布\n"
    for source, count in trend_analysis['source_distribution'].items():
        percentage = (count / trend_analysis['total_news'] * 100) if trend_analysis['total_news'] else 0
        report += f"- {source}: {count} ({percentage:.1f}%)\n"
    report += "\n"
    
    report += f"## 热门关键词\n"
    for keyword, weight in trend_analysis['top_keywords'][:10]:
        report += f"- {keyword}: {weight:.3f}\n"
    report += "\n"
    
    report += f"## 趋势分析\n"
    if trend_analysis['ai_news_percentage'] > 50:
        report += "- 今日新闻以AI相关内容为主，人工智能技术是热点话题\n"
    elif trend_analysis['tech_news_percentage'] > 50:
        report += "- 今日新闻以科技相关内容为主，技术发展是热点话题\n"
    else:
        report += "- 今日新闻内容较为多样化，没有明显的热点方向\n"
    
    return report

def analyze_news_sentiment(news_items: List[Dict]) -> Dict:
    """
    分析新闻情感倾向
    :param news_items: 新闻列表
    :return: 情感分析结果
    """
    # 简单的情感分析
    positive_words = ['成功', '提升', '创新', '突破', '发布', '推出', '增长', '发展', '进步', '优势']
    negative_words = ['问题', '风险', '挑战', '下降', '失败', '漏洞', '安全', '威胁', '危机', '亏损']
    
    sentiment_counts = {
        'positive': 0,
        'negative': 0,
        'neutral': 0
    }
    
    for news in news_items:
        text = news.get('title', '') + " " + news.get('summary', '')
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            sentiment_counts['positive'] += 1
        elif negative_count > positive_count:
            sentiment_counts['negative'] += 1
        else:
            sentiment_counts['neutral'] += 1
    
    return sentiment_counts

if __name__ == "__main__":
    # 测试数据
    test_news = [
        {
            'title': 'OpenAI发布GPT-5模型，性能大幅提升',
            'summary': 'OpenAI今日发布了全新的GPT-5模型，性能相比GPT-4有了大幅提升，支持更多语言和更复杂的任务。',
            'source': 'IT之家'
        },
        {
            'title': '华为发布全新Mate 60 Pro手机',
            'summary': '华为今日发布了全新的Mate 60 Pro手机，搭载了最新的麒麟芯片，性能强劲。',
            'source': '36氪'
        }
    ]
    
    # 分析趋势
    trend_analysis = analyze_news_trends(test_news)
    print(trend_analysis)
    
    # 生成报告
    report = generate_trend_report(trend_analysis)
    print(report)
    
    # 分析情感
    sentiment = analyze_news_sentiment(test_news)
    print(sentiment)