import os
import schedule
import time
from main import main

def run_daily_update():
    """每日更新函数"""
    print("开始执行每日新闻更新...")
    main()
    print("每日新闻更新完成！")

def setup_schedule():
    """设置定时任务"""
    # 每天早上8点执行更新
    schedule.every().day.at("08:00").do(run_daily_update)
    
    print("定时任务已设置，每天早上8点执行新闻更新")
    print("按 Ctrl+C 退出程序")
    
    # 运行一次初始更新
    run_daily_update()
    
    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    setup_schedule()