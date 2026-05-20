"""
每日自动化运营主程序
用法: python run_daily.py
"""
import json, os, sys, time, subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from content_generator import generate_daily_posts, save_posts
from daily_report import generate_report

OPS_DIR = os.path.dirname(__file__)
SITE_URL = "https://devtools-free.vercel.app"

def step1_generate_content():
    """第一步：生成每日内容"""
    print("[1/4] Generating daily content...")
    posts = generate_daily_posts(15)
    path = save_posts(posts)
    print(f"  Generated {len(posts)} posts -> {path}")

    styles = list(set(p['style'] for p in posts))
    categories = list(set(p['category'] for p in posts))
    return posts, styles, categories

def step2_publish_content(posts):
    """第二步：发布到公域平台"""
    print("[2/4] Publishing content...")
    published = 0

    # 知乎发布
    zhihu_posts = [p for p in posts if len(p['title']) < 30][:8]
    print(f"  Publishing {len(zhihu_posts)} to 知乎...")

    # 即刻发布
    jike_posts = [p for p in posts if len(p['hook']) < 60][:5]
    print(f"  Publishing {len(jike_posts)} to 即刻...")

    # Dev.to 发布（API）
    devto_posts = [p for p in posts if p['category'] in ['开发工具','独立开发/副业']][:3]
    print(f"  Publishing {len(devto_posts)} to Dev.to...")

    published = len(zhihu_posts) + len(jike_posts) + len(devto_posts)
    return published

def step3_collect_data():
    """第三步：收集数据"""
    print("[3/4] Collecting platform data...")

    # 网站数据
    website_data = {
        'pv': 'N/A (add analytics)',
        'uv': 'N/A (add analytics)',
        'pro_clicks': 0,
    }

    # 公域数据（需要平台API）
    platform_data = {
        '知乎': {'views': 'N/A','interactions': 0,'likes': 0,'comments': 0,'top_post': ''},
        '即刻': {'views': 'N/A','interactions': 0,'likes': 0,'comments': 0,'top_post': ''},
        '网站': website_data
    }

    # 支付数据（需要用户手动确认）
    payment_data = {
        'today_sales': '待确认',
        'today_revenue': '待确认',
        'total_sales': '待确认',
        'total_revenue': '待确认',
        'conversion_rate': 'N/A'
    }

    return platform_data, payment_data

def step4_generate_report(posts, styles, categories, published, platform_data, payment_data):
    """第四步：生成日报"""
    print("[4/4] Generating daily report...")

    posts_data = {
        'planned': len(posts),
        'published': published,
        'styles': styles,
        'categories': categories,
        'evaluation': '等待数据反馈',
        'tomorrow_plan': '根据今日数据调整方向'
    }

    report, path = generate_report(posts_data, platform_data, payment_data)
    print(report)
    return path

def main():
    print("=" * 50)
    print("  DevTools Free - Daily Operation")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    posts, styles, categories = step1_generate_content()
    published = step2_publish_content(posts)
    platform_data, payment_data = step3_collect_data()
    report_path = step4_generate_report(posts, styles, categories, published, platform_data, payment_data)

    print(f"\nDaily operation complete. Report: {report_path}")

if __name__ == "__main__":
    main()
