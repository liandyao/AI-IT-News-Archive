import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from typing import Dict, List
import os

def plot_news_category_pie(trend_analysis: Dict, output_path: str):
    """
    绘制新闻分类饼图
    :param trend_analysis: 趋势分析结果
    :param output_path: 输出文件路径
    """
    try:
        # 准备数据
        labels = ['AI新闻', '科技新闻', '其他新闻']
        sizes = [
            trend_analysis['ai_news_count'],
            trend_analysis['tech_news_count'],
            trend_analysis['other_news_count']
        ]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        # 创建图表
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('新闻分类分布')
        
        # 保存图表
        plt.savefig(output_path)
        plt.close()
        print(f"新闻分类饼图已保存到: {output_path}")
    except Exception as e:
        print(f"绘制新闻分类饼图时出错: {e}")

def plot_source_distribution_bar(trend_analysis: Dict, output_path: str):
    """
    绘制来源分布柱状图
    :param trend_analysis: 趋势分析结果
    :param output_path: 输出文件路径
    """
    try:
        # 准备数据
        sources = list(trend_analysis['source_distribution'].keys())
        counts = list(trend_analysis['source_distribution'].values())
        
        # 创建图表
        plt.figure(figsize=(10, 6))
        plt.bar(sources, counts, color='#66b3ff')
        plt.xlabel('新闻来源')
        plt.ylabel('新闻数量')
        plt.title('新闻来源分布')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # 保存图表
        plt.savefig(output_path)
        plt.close()
        print(f"来源分布柱状图已保存到: {output_path}")
    except Exception as e:
        print(f"绘制来源分布柱状图时出错: {e}")

def generate_wordcloud(keywords: List, output_path: str):
    """
    生成关键词词云
    :param keywords: 关键词列表，每个元素是(关键词, 权重)元组
    :param output_path: 输出文件路径
    """
    try:
        # 准备数据
        word_dict = {keyword: weight for keyword, weight in keywords}
        
        # 创建词云
        wordcloud = WordCloud(
            width=800,
            height=600,
            background_color='white',
            font_path='C:\\Windows\\Fonts\\simhei.ttf'  # 使用中文字体
        ).generate_from_frequencies(word_dict)
        
        # 保存词云
        wordcloud.to_file(output_path)
        print(f"关键词词云已保存到: {output_path}")
    except Exception as e:
        print(f"生成关键词词云时出错: {e}")

def plot_sentiment_pie(sentiment_counts: Dict, output_path: str):
    """
    绘制情感分析饼图
    :param sentiment_counts: 情感分析结果
    :param output_path: 输出文件路径
    """
    try:
        # 准备数据
        labels = ['积极', '消极', '中性']
        sizes = [
            sentiment_counts.get('positive', 0),
            sentiment_counts.get('negative', 0),
            sentiment_counts.get('neutral', 0)
        ]
        colors = ['#99ff99', '#ff9999', '#66b3ff']
        
        # 创建图表
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('新闻情感分布')
        
        # 保存图表
        plt.savefig(output_path)
        plt.close()
        print(f"情感分析饼图已保存到: {output_path}")
    except Exception as e:
        print(f"绘制情感分析饼图时出错: {e}")

def generate_all_visualizations(trend_analysis: Dict, sentiment_counts: Dict, output_dir: str):
    """
    生成所有可视化图表
    :param trend_analysis: 趋势分析结果
    :param sentiment_counts: 情感分析结果
    :param output_dir: 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成各种图表
    plot_news_category_pie(trend_analysis, os.path.join(output_dir, 'news_category_pie.png'))
    plot_source_distribution_bar(trend_analysis, os.path.join(output_dir, 'source_distribution_bar.png'))
    generate_wordcloud(trend_analysis['top_keywords'], os.path.join(output_dir, 'keywords_wordcloud.png'))
    plot_sentiment_pie(sentiment_counts, os.path.join(output_dir, 'sentiment_pie.png'))
    
    print("所有可视化图表已生成")

if __name__ == "__main__":
    # 测试数据
    test_trend_analysis = {
        'total_news': 10,
        'ai_news_count': 3,
        'tech_news_count': 6,
        'other_news_count': 1,
        'top_keywords': [('AI', 0.9), ('科技', 0.8), ('手机', 0.7), ('智能', 0.6), ('技术', 0.5)],
        'source_distribution': {'IT之家': 8, '36氪': 2}
    }
    
    test_sentiment_counts = {
        'positive': 6,
        'negative': 1,
        'neutral': 3
    }
    
    # 生成可视化
    output_dir = os.path.join(os.getcwd(), 'visualizations')
    generate_all_visualizations(test_trend_analysis, test_sentiment_counts, output_dir)