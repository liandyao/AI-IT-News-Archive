from openai import OpenAI
import os
from typing import List, Dict

class QwenLLM:
    def __init__(self, api_key: str):
        """
        初始化Qwen LLM
        :param api_key: API密钥
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.scnet.cn/api/llm/v1"
        )
    
    def generate_summary(self, news_title: str, news_source: str) -> str:
        """
        使用Qwen LLM生成新闻摘要
        :param news_title: 新闻标题
        :param news_source: 新闻来源
        :return: 生成的摘要
        """
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的新闻摘要助手，需要对新闻标题进行简洁准确的摘要，突出核心内容和重要信息。"},
                {"role": "user", "content": f"请为以下新闻标题生成一个简短的摘要，来源是{news_source}：{news_title}"}
            ]
            
            completion = self.client.chat.completions.create(
                model="Qwen3-30B-A3B",
                messages=messages,
                temperature=0.3,
                max_tokens=100
            )
            
            summary = completion.choices[0].message.content
            if summary:
                return summary.strip()
            else:
                # 当返回内容为None时的处理
                return f"这是一条来自{news_source}的新闻，标题为{news_title}，可能包含相关领域的最新动态。"
        except Exception as e:
            print(f"调用Qwen LLM API时出错: {e}")
            # 降级到基于规则的摘要
            return f"这是一条来自{news_source}的新闻，标题为{news_title}，可能包含相关领域的最新动态。"

def summarize_news_with_qwen(news_items: List[Dict], api_key: str) -> List[Dict]:
    """
    使用Qwen LLM总结新闻内容
    :param news_items: 新闻列表
    :param api_key: Qwen API密钥
    :return: 带有摘要的新闻列表
    """
    llm = QwenLLM(api_key)
    summarized_news = []
    
    for news in news_items:
        title = news.get('title', '')
        source = news.get('source', '')
        link = news.get('link', '')
        
        # 使用Qwen LLM生成摘要
        summary = llm.generate_summary(title, source)
        
        summarized_news.append({
            'title': title,
            'link': link,
            'source': source,
            'summary': summary
        })
    
    return summarized_news

def analyze_news_with_qwen(summarized_news: List[Dict], api_key: str) -> str:
    """
    使用Qwen LLM分析新闻趋势
    :param summarized_news: 带有摘要的新闻列表
    :param api_key: Qwen API密钥
    :return: 趋势分析报告
    """
    llm = QwenLLM(api_key)
    
    # 收集所有新闻摘要
    all_summaries = "\n".join([f"{news['title']}: {news['summary']}" for news in summarized_news])
    
    # 构建分析请求
    analysis_prompt = f"请分析以下IT和AI新闻的趋势，包括：\n1. 主要热点话题\n2. 技术发展趋势\n3. 行业动态\n4. 重要事件总结\n\n新闻内容：\n{all_summaries}"
    
    try:
        messages = [
            {"role": "system", "content": "你是一个专业的新闻分析师，擅长分析IT和AI领域的新闻趋势，能够从大量新闻中提取关键信息并进行深度分析。"},
            {"role": "user", "content": analysis_prompt}
        ]
        
        completion = llm.client.chat.completions.create(
            model="Qwen3-30B-A3B",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        
        analysis = completion.choices[0].message.content
        if analysis:
            return analysis.strip()
        else:
            return "无法生成趋势分析，请稍后再试。"
    except Exception as e:
        print(f"调用Qwen LLM进行趋势分析时出错: {e}")
        return "无法生成趋势分析，请稍后再试。"

if __name__ == "__main__":
    # 测试数据
    test_news = [
        {
            'title': 'OpenAI发布GPT-5模型，性能大幅提升',
            'link': 'https://example.com/news1',
            'source': 'IT之家',
            'date': '2026-03-11'
        }
    ]
    
    # 这里需要填写真实的API密钥
    api_key = "sk-MjczLTExMTc0MTY2NjIzLTE3NzMzMTY2NjQ2MjU="
    summarized = summarize_news_with_qwen(test_news, api_key)
    print(summarized)