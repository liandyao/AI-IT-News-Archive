import requests
import feedparser
import datetime
import time

# 新闻网站RSS配置
NEWS_RSS = {
    'IT之家': {
        'url': 'https://www.ithome.com/rss/',
        'keywords': ['AI', '人工智能', '科技', 'IT']
    },
    '36氪': {
        'url': 'https://36kr.com/feed',
        'keywords': ['AI', '人工智能', '科技', 'IT']
    },
    '少数派': {
        'url': 'https://sspai.com/feed',
        'keywords': ['AI', '人工智能', '科技', 'IT']
    }
}

def get_todays_date():
    """获取今天的日期，格式为YYYY-MM-DD"""
    return datetime.datetime.now().strftime('%Y-%m-%d')

def fetch_news_from_rss(site_name, rss_config):
    """从RSS订阅获取新闻"""
    try:
        print(f"正在从{site_name}的RSS获取新闻...")
        response = requests.get(rss_config['url'], timeout=15)
        response.raise_for_status()
        
        # 解析RSS
        feed = feedparser.parse(response.content)
        
        today = get_todays_date()
        todays_news = []
        
        # 处理新闻条目
        for entry in feed.entries[:20]:  # 只处理前20条
            try:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                pub_date = entry.get('published', '')
                
                # 过滤条件
                if not title or not link or len(title) < 10:
                    continue
                
                # 检查是否包含关键词
                has_keyword = any(keyword in title for keyword in rss_config['keywords'])
                
                # 对于少数派，只保留科技相关内容
                if site_name == '少数派' and not has_keyword:
                    continue
                
                # 添加新闻到列表
                todays_news.append({
                    'title': title,
                    'link': link,
                    'date': pub_date,
                    'source': site_name
                })
                
                if len(todays_news) >= 10:  # 每个网站最多抓取10条
                    break
            except Exception as e:
                continue
        
        print(f"{site_name}成功获取{len(todays_news)}条新闻")
        return todays_news
    except Exception as e:
        print(f"从{site_name}获取新闻时出错: {e}")
        return []

def fetch_all_news():
    """获取所有网站的新闻"""
    all_news = []
    
    for site_name, rss_config in NEWS_RSS.items():
        news = fetch_news_from_rss(site_name, rss_config)
        all_news.extend(news)
        time.sleep(1)  # 避免请求过于频繁
    
    return all_news

if __name__ == "__main__":
    today = get_todays_date()
    print(f"开始获取{today}的IT和AI新闻...")
    
    news = fetch_all_news()
    
    print(f"\n共获取到{len(news)}条新闻:")
    for i, item in enumerate(news, 1):
        print(f"{i}. {item['title']} - {item['source']}")
        print(f"   链接: {item['link']}")
        if item.get('date'):
            print(f"   日期: {item['date']}")
        print()