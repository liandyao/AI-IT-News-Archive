# 测试摘要生成功能
import os
from qwen_llm import QwenLLM

# 测试数据 - 模拟RSS获取的新闻
test_news = {
    'title': '微信鸿蒙版 App 扫码登录手表端要求公布，手机系统需升级至 HarmonyOS 6.0.0.130 及以上版本',
    'source': 'IT之家',
    'link': 'https://www.ithome.com/0/928/546.htm',
    'description': '''IT之家 3 月 12 日消息，微信鸿蒙版今日（3 月 12 日）迎来 8.0.15.64 正式版更新，官方更新日志为"修复了一些已知问题"。

目前，微信鸿蒙版 App 扫码登录手表端正陆续开放。IT之家就微信手表版相关问题咨询了华为终端客服，对方给出了功能支持要求及适配情况：

HarmonyOS 5 及以上版本手机登录手表微信功能微信侧正在分批开放中，请您将 HarmonyOS 手机系统升级至 6.0.0.130 及以上版本，手机微信升级至 8.0.15.49 及以上版本后等待功能开放。

功能开放后，您用手机微信扫描手表微信登录二维码即可登录体验，如仍提示暂不支持登录或微信版本较低，说明当前暂时还未开放。

微信鸿蒙版 App 于去年 1 月正式登陆华为鸿蒙应用市场 App Gallery，已支持基础通讯、社交、微信支付、公众号、小程序、视频号、直播等主要功能。另外，微信鸿蒙版安装量已超 4008 万次，微信支付也正式接入鸿蒙 5 收银台，用户购买数字商品时，可选用微信支付进行结算。'''
}

# 测试LLM摘要生成
api_key = os.environ.get('QWEN_API_KEY', 'sk-MjczLTExMTc0MTY2NjIzLTE3NzMzMTY2NjQ2MjU=')
llm = QwenLLM(api_key)

print("测试新闻标题:")
print(test_news['title'])
print("\n" + "="*50)
print("\n生成的摘要:")
summary = llm.generate_summary(
    test_news['title'], 
    test_news['source'], 
    test_news['description']
)
print(summary)
