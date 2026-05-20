"""
每日内容生成器 - 10-20条不同风格的引流内容
"""
import random, json, os, time
from datetime import datetime

SITE_URL = "https://devtools-free.vercel.app"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ops', 'daily_output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 10种不同风格模板
STYLES = [
    "工具实测",    # 真实使用感受，有细节
    "认知颠覆",    # 反常识观点
    "故事体",      # 个人经历切入
    "合集体",      # 5个/10个推荐清单
    "教程体",      # 如何做某事的步骤
    "对比体",      # A vs B 对比
    "避坑体",      # 踩过的坑
    "数据体",      # 用数据说话
    "提问体",      # 抛问题引发讨论
    "情绪体",      # 情绪化表达，引发共鸣
]

# 内容主题库
TOPICS = {
    "AI工具": [
        {"title": "用了3个月AI工具后的真实感受", "angle": "不是神化也不是贬低，说点大实话", "keywords": ["AI工具","效率","实话"]},
        {"title": "这5个免费AI工具每天都在用", "angle": "打工人必备效率工具清单", "keywords": ["免费AI","效率工具","推荐"]},
        {"title": "被AI写周报的速度惊到了", "angle": "具体演示AI怎么帮我写周报", "keywords": ["AI写作","周报","效率"]},
        {"title": "同样用AI，为什么别人产出比你高3倍", "angle": "差距不在工具，在提问方式", "keywords": ["AI技巧","效率差距","Prompt"]},
        {"title": "别再花钱买AI课程了", "angle": "真正有用的AI技能就这几个", "keywords": ["AI学习","省钱","干货"]},
        {"title": "我让4个AI写同一份方案，结果差距巨大", "angle": "实测对比ChatGPT/Claude/DeepSeek/Kimi", "keywords": ["AI对比","测评","实测"]},
        {"title": "用了半年AI后我发现的一个真相", "angle": "AI让强者更强，让懒人更懒", "keywords": ["AI真相","职场","思考"]},
        {"title": "打工人用AI省下的时间可以做什么", "angle": "不是去做更多工作，是做更重要的事", "keywords": ["效率","AI","职场"]},
        {"title": "每天花15分钟学AI，一个月后的变化", "angle": "循序渐进的学习路径", "keywords": ["AI学习","坚持","成长"]},
        {"title": "为什么你让AI写的文案总像机器人", "angle": "因为你给指令的方式不对", "keywords": ["AI写作","Prompt","技巧"]},
    ],
    "开发工具": [
        {"title": "JSON格式化这种小工具为什么还有人做", "angle": "因为大厂不做，小需求没人管", "keywords": ["JSON","工具","独立开发"]},
        {"title": "发现一个超好用的免费在线工具站", "angle": "程序员必备，不用安装任何东西", "keywords": ["在线工具","免费","推荐"]},
        {"title": "周末做了一个工具站，没想到真有人用", "angle": "独立开发从0到1的真实经历", "keywords": ["独立开发","工具站","副业"]},
        {"title": "这10个工具让我的开发效率翻倍", "angle": "从写代码到部署，每个环节的工具推荐", "keywords": ["开发工具","效率","程序员"]},
        {"title": "为什么我不用VS Code插件而用在线工具", "angle": "跨设备、不占内存、不收集数据", "keywords": ["在线工具","VS Code","隐私"]},
        {"title": "5分钟搭一个免费工具站，不用买服务器", "angle": "Vercel+GitHub的免费部署方案", "keywords": ["免费部署","Vercel","独立开发"]},
        {"title": "独立开发3个月，我的工具站每天100+访问", "angle": "从选品到推广的完整复盘", "keywords": ["独立开发","复盘","SEO"]},
        {"title": "程序员副业不一定非要接外包", "angle": "做工具站是性价比更高的选择", "keywords": ["副业","独立开发","程序员"]},
        {"title": "一个JSON格式化工具，凭什么让人付费", "angle": "免费的够用，但PRO有特殊价值", "keywords": ["工具付费","PRO","价值"]},
        {"title": "你常用的在线工具站可能明天就没了", "angle": "为什么独立工具站比大厂产品更靠谱", "keywords": ["工具站","独立开发","持久"]},
    ],
    "独立开发/副业": [
        {"title": "做了3个副业方向后，终于有一个稳定出单了", "angle": "试错是必经之路", "keywords": ["副业","试错","独立开发"]},
        {"title": "下班后2小时能做的一个数字产品", "angle": "每天投入2小时，2周出一个产品", "keywords": ["副业","数字产品","时间管理"]},
        {"title": "5块钱的工具PRO，有人买吗？实测数据告诉你", "angle": "低价策略的付费转化率", "keywords": ["定价","PRO","转化率"]},
        {"title": "收入从0到100块用了2个月，但值得", "angle": "独立开发的前期积累期", "keywords": ["独立开发","收入","坚持"]},
        {"title": "不上班靠什么养活自己", "angle": "独立开发者的收入结构拆解", "keywords": ["自由职业","独立开发","收入"]},
        {"title": "为什么说工具站是程序员最好的副业", "angle": "一次开发，持续收入，边际成本为零", "keywords": ["工具站","副业","程序员"]},
        {"title": "一年做了20个小工具，分享我的选品逻辑", "angle": "选什么做、不做什么的决策框架", "keywords": ["选品","工具","方法论"]},
        {"title": "独立开发者最怕的不是没技术", "angle": "是没有用户反馈", "keywords": ["独立开发","用户","反馈"]},
        {"title": "做产品的正确顺序：先卖再做", "angle": "验证需求再写代码", "keywords": ["产品","需求验证","独立开发"]},
        {"title": "一个人的团队怎么做到日更内容", "angle": "自动化内容生产的流程分享", "keywords": ["自动化","内容","效率"]},
    ],
    "效率/职场": [
        {"title": "每天只做3件事，工作效率反而翻倍了", "angle": "少即是多的具体实践", "keywords": ["效率","时间管理","职场"]},
        {"title": "上班第三年才学会的摸鱼方式", "angle": "不是偷懒，是聪明的精力分配", "keywords": ["职场","效率","摸鱼"]},
        {"title": "老板以为我加班，其实我用了这些工具", "angle": "效率工具让工作时间缩短一半", "keywords": ["效率工具","职场","打工人"]},
        {"title": "为什么有些人看起来毫不费力", "angle": "不是天赋，是有一套效率系统", "keywords": ["效率","系统","方法"]},
        {"title": "这3个习惯让我从天天加班到准时下班", "angle": "具体可操作的习惯养成方法", "keywords": ["习惯","效率","职场"]},
    ],
}

def generate_daily_posts(count=15):
    """生成每日内容池"""
    posts = []
    all_items = []
    for category, items in TOPICS.items():
        for item in items:
            all_items.append({"category": category, **item})

    random.shuffle(all_items)
    selected = all_items[:count]

    for item in selected:
        style = random.choice(STYLES)
        # 生成不同风格的变体
        hooks = {
            "工具实测": f"实测{item['title']}",
            "认知颠覆": f"90%的人不知道：{item['angle']}",
            "故事体": f"我的{item['keywords'][0]}故事：{item['title']}",
            "合集体": f"推荐{item['keywords']}相关的{item['title']}",
            "教程体": f"手把手教你{item['title']}",
            "对比体": f"对比了{item['keywords'][0]}才发现：{item['title']}",
            "避坑体": f"踩过坑才敢说：{item['title']}",
            "数据体": f"数据告诉你：{item['title']}",
            "提问体": f"你们觉得{item['keywords'][0]}真的有用吗？",
            "情绪体": f"被{item['keywords'][0]}惊到了！{item['title']}",
        }

        post = {
            "title": item['title'][:50],
            "hook": hooks.get(style, item['title']),
            "style": style,
            "category": item['category'],
            "keywords": item['keywords'],
            "angle": item['angle'],
            "cta": f"试试这个免费工具站 {SITE_URL}",
            "generated_at": datetime.now().isoformat()
        }
        posts.append(post)

    return posts

def save_posts(posts):
    """保存当日内容"""
    today = datetime.now().strftime("%Y%m%d")
    path = os.path.join(OUTPUT_DIR, f"posts_{today}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    return path

if __name__ == "__main__":
    posts = generate_daily_posts(15)
    path = save_posts(posts)
    print(f"Generated {len(posts)} posts -> {path}")
    for i, p in enumerate(posts[:5]):
        print(f"  [{p['style']}] {p['title'][:40]}...")
