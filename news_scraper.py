import requests
import feedparser
import datetime
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 新闻网站RSS配置
NEWS_RSS = {
    'IT之家': {
        'url': 'https://www.ithome.com/rss/' 
    },
    '36氪': {
        'url': 'https://36kr.com/feed' 
    }  
}

def get_beijing_time():
    """
    获取东八区（北京时间）
    :return: 北京时间
    """
    from datetime import timezone, timedelta
    utc_now = datetime.datetime.now(timezone.utc)
    beijing_tz = timezone(timedelta(hours=8))
    return utc_now.astimezone(beijing_tz)

def get_todays_date():
    """获取今天的日期，格式为YYYY-MM-DD"""
    return get_beijing_time().strftime('%Y-%m-%d')

def fetch_news_from_rss(site_name, rss_config):
    """从RSS订阅获取新闻"""
    try:
        logging.info(f"正在从{site_name}的RSS获取新闻...")
        
        # 添加请求头，模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        
        # 尝试3次
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(rss_config['url'], timeout=20, headers=headers)
                response.raise_for_status()
                logging.info(f"成功获取{site_name}的RSS内容，状态码: {response.status_code}")
                break
            except requests.RequestException as e:
                logging.warning(f"第{attempt+1}次尝试获取{site_name}失败: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    raise
        
        # 解析RSS
        feed = feedparser.parse(response.content)
        logging.info(f"解析{site_name}的RSS，获取到{len(feed.entries)}条条目")
        
        today = get_todays_date()
        todays_news = []
        
        # 处理新闻条目
        for i, entry in enumerate(feed.entries):
            try:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                pub_date = entry.get('published', '')
                
                # 过滤条件
                if not title or not link or len(title) < 10:
                    logging.debug(f"跳过无效新闻: {title}")
                    continue
              
                # 获取新闻内容/描述
                description = entry.get('description', '').strip()
                # 清理HTML标签
                if description:
                    import re
                    description = re.sub('<[^<]+?>', '', description)
                    description = description[:1000]  # 限制长度
                
                # 添加新闻到列表
                todays_news.append({
                    'title': title,
                    'link': link,
                    'date': pub_date,
                    'source': site_name,
                    'description': description
                })
                
                if i < 5:  # 只显示前5条作为示例
                    logging.info(f"获取到{site_name}新闻: {title}")
                
            except Exception as e:
                logging.error(f"处理{site_name}新闻时出错: {e}")
                continue
        
        logging.info(f"{site_name}成功获取{len(todays_news)}条新闻")
        return todays_news
    except Exception as e:
        logging.error(f"从{site_name}获取新闻时出错: {e}")
        return []

def fetch_all_news():
    """获取所有网站的新闻"""
    all_news = []
    
    for site_name, rss_config in NEWS_RSS.items():
        news = fetch_news_from_rss(site_name, rss_config)
        all_news.extend(news)
        time.sleep(2)  # 增加等待时间，避免请求过于频繁
    
    logging.info(f"总共获取到{len(all_news)}条新闻")
    return all_news

if __name__ == "__main__":
    today = get_todays_date()
    logging.info(f"开始获取{today}的IT和AI新闻...")
    
    news = fetch_all_news()
    
    logging.info(f"\n共获取到{len(news)}条新闻:")
    for i, item in enumerate(news, 1):
        print(f"{i}. {item['title']} - {item['source']}")
        print(f"   链接: {item['link']}")
        if item.get('date'):
            print(f"   日期: {item['date']}")
        print()
