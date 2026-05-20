"""
每日运营日报生成器
"""
import json, os, time
from datetime import datetime, timedelta

REPORT_DIR = os.path.join(os.path.dirname(__file__), 'daily_output')
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_report(posts_data, platform_data, payment_data):
    """生成日报"""
    today = datetime.now().strftime("%Y-%m-%d")

    report = f"""
========================================
  DevTools Free 运营日报 - {today}
========================================

【内容发布】
  计划发布: {posts_data.get('planned', 0)} 条
  实际发布: {posts_data.get('published', 0)} 条
  覆盖风格: {', '.join(posts_data.get('styles', []))}
  覆盖主题: {', '.join(posts_data.get('categories', []))}

【公域数据】
"""
    for platform, stats in platform_data.items():
        report += f"  {platform}:\n"
        report += f"    浏览量: {stats.get('views', 0)}\n"
        report += f"    互动数: {stats.get('interactions', 0)}\n"
        report += f"    点赞: {stats.get('likes', 0)}\n"
        report += f"    评论: {stats.get('comments', 0)}\n"
        if stats.get('top_post'):
            report += f"    最佳内容: {stats['top_post'][:50]}...\n"

    report += f"""
【成交数据】
  今日付费: {payment_data.get('today_sales', 0)} 笔
  今日收入: ¥{payment_data.get('today_revenue', 0)}
  累计付费: {payment_data.get('total_sales', 0)} 笔
  累计收入: ¥{payment_data.get('total_revenue', 0)}
  PRO转化率: {payment_data.get('conversion_rate', '0%')}

【网站数据】
  今日PV: {platform_data.get('website', {}).get('pv', 'N/A')}
  今日UV: {platform_data.get('website', {}).get('uv', 'N/A')}
  PRO点击: {platform_data.get('website', {}).get('pro_clicks', 0)}

【效果评估】
  {posts_data.get('evaluation', '待评估')}

【明日计划】
  {posts_data.get('tomorrow_plan', '继续优化内容，扩大曝光')}

========================================
  报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
"""
    # 保存
    path = os.path.join(REPORT_DIR, f"report_{today.replace('-','')}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)

    # 追加到汇总
    summary_path = os.path.join(REPORT_DIR, "all_reports.txt")
    with open(summary_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*40}\n{today}\n{'='*40}\n")
        f.write(f"发布: {posts_data.get('published', 0)}条 | ")
        f.write(f"互动: {sum(s.get('interactions',0) for s in platform_data.values())} | ")
        f.write(f"付费: ¥{payment_data.get('today_revenue', 0)}\n")

    return report, path

if __name__ == "__main__":
    # 示例数据
    report, path = generate_report(
        posts_data={
            'planned': 15, 'published': 12,
            'styles': ['工具实测','故事体','合集体'],
            'categories': ['AI工具','开发工具','独立开发'],
            'evaluation': '3条有互动，流量在增长',
            'tomorrow_plan': '加大AI工具方向内容'
        },
        platform_data={
            '知乎': {'views': 320, 'interactions': 15, 'likes': 8, 'comments': 3, 'top_post': '被AI写周报速度惊到'},
            '网站': {'pv': 156, 'uv': 89, 'pro_clicks': 4}
        },
        payment_data={
            'today_sales': 0, 'today_revenue': 0, 'total_sales': 0, 'total_revenue': 0,
            'conversion_rate': '2.5%'
        }
    )
    print(report)
