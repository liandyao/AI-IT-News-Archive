from openai import OpenAI, RateLimitError
import os
import time
import random
from typing import List, Dict

class QwenLLM:
    def __init__(self, api_key: str):
        """
        初始化Qwen LLM
        :param api_key: API密钥
        """
        self.api_key = api_key
        self.base_url = "https://api.scnet.cn/api/llm/v1"
        # 创建OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def generate_summary(self, news_title: str, news_source: str, description: str = "") -> str:
        """
        使用Qwen LLM生成新闻摘要
        :param news_title: 新闻标题
        :param news_source: 新闻来源
        :param description: 新闻描述/内容
        :return: 生成的摘要
        """
        # 构建提示词
        if description and len(description) > 50:
            messages = [
                {"role": "system", "content": "你是一个专业的新闻摘要助手。请直接返回摘要，不要包含任何思考过程。根据提供的新闻标题和正文内容，生成一个简洁准确的摘要（2-3句话），突出核心信息、关键数据和重要结论。不要简单重复标题。"},
                {"role": "user", "content": f"新闻：\n标题：{news_title}\n内容：{description[:800]}\n\n请直接返回摘要："}
            ]
        else:
            messages = [
                {"role": "system", "content": "你是一个专业的新闻摘要助手。请直接返回摘要，不要包含任何思考过程。根据新闻标题，推测并生成一个简洁准确的摘要（1-2句话），突出可能的核心内容。"},
                {"role": "user", "content": f"新闻标题：{news_title}\n\n请直接返回摘要："}
            ]
        
        # 调用API，使用stream=False，带重试机制
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="Qwen3-30B-A3B",
                    messages=messages,
                    stream=False
                )
                # 打印完整响应，用于调试
                print("\nAPI响应:")
                print(response)
                
                # 提取摘要
                summary = response.choices[0].message.content
                if summary:
                    return summary.strip()
                else:
                    return "摘要生成失败，请检查API配置"
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"速率限制错误，等待 {wait_time:.2f} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("达到最大重试次数，返回失败")
                    return "摘要生成失败：API速率限制"
            except Exception as e:
                print(f"API调用失败: {str(e)}")
                return f"摘要生成失败：{str(e)}"


def summarize_news_with_qwen(news_items: List[Dict], api_key: str) -> List[Dict]:
    """
    使用Qwen LLM总结新闻内容
    :param news_items: 新闻列表
    :param api_key: Qwen API密钥
    :return: 带有摘要的新闻列表
    """
    llm = QwenLLM(api_key)
    summarized_news = []
    
    for i, news in enumerate(news_items):
        title = news.get('title', '')
        source = news.get('source', '')
        link = news.get('link', '')
        description = news.get('description', '')
        
        print(f"处理第 {i+1} 条新闻: {title}")
        
        # 使用Qwen LLM生成摘要，传入description
        summary = llm.generate_summary(title, source, description)
        
        summarized_news.append({
            'title': title,
            'link': link,
            'source': source,
            'summary': summary
        })
        
        # 添加60秒延迟，确保每分钟只请求一条数据
        if i < len(news_items) - 1:  # 最后一条新闻后不需要延迟
            print("等待60秒后处理下一条新闻...")
            time.sleep(60)
    
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
    
    messages = [
        {"role": "system", "content": "你是一个专业的新闻分析师，擅长分析IT和AI领域的新闻趋势，能够从大量新闻中提取关键信息并进行深度分析。"},
        {"role": "user", "content": analysis_prompt}
    ]
    
    # 调用API，带重试机制
    max_retries = 5
    for attempt in range(max_retries):
        try:
            completion = llm.client.chat.completions.create(
                model="Qwen3-30B-A3B",
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            
            message = completion.choices[0].message
            # 检查content字段
            if hasattr(message, 'content') and message.content:
                return message.content.strip()
            else:
                return "趋势分析生成失败，请检查API配置"
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"速率限制错误，等待 {wait_time:.2f} 秒后重试...")
                time.sleep(wait_time)
            else:
                print("达到最大重试次数，返回失败")
                return "趋势分析生成失败：API速率限制"
        except Exception as e:
            print(f"API调用失败: {str(e)}")
            return f"趋势分析生成失败：{str(e)}"


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
    api_key = os.environ.get('QWEN_API_KEY')
    summarized = summarize_news_with_qwen(test_news, api_key)
    print(summarized)