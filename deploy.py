"""
全自动部署 + 运维脚本
首次使用：python deploy.py --setup
日常更新：python deploy.py
"""
import os, sys, json, subprocess, hashlib, time, http.server, threading

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEPLOY_LOG = os.path.join(PROJECT_DIR, 'deploy-log.json')

def log(msg):
    print(f'[{time.strftime("%H:%M:%S")}] {msg}')

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_DIR)
    if result.returncode != 0:
        log(f'ERROR: {result.stderr[:200]}')
    return result

def verify_local():
    """验证本地工具站功能"""
    log('Verifying local build...')

    # Check index.html exists and is valid
    index_path = os.path.join(PROJECT_DIR, 'index.html')
    if not os.path.exists(index_path):
        log('ERROR: index.html not found')
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Verify key features
    checks = [
        ('JSON formatter', 'formatJSON' in html),
        ('AI writer', 'generateAI' in html),
        ('PRO upgrade', 'buyPro' in html),
        ('Responsive', 'viewport' in html),
        ('SEO meta', 'description' in html.lower()),
    ]
    for name, ok in checks:
        log(f'  {name}: {"OK" if ok else "MISSING"}')

    return all(ok for _, ok in checks)

def deploy_vercel():
    """通过Vercel CLI部署（需要先vercel login）"""
    log('Deploying to Vercel...')

    # Check if vercel is authenticated
    result = run('vercel whoami')
    if result.returncode != 0:
        log('Vercel not authenticated. Run: vercel login')
        return False

    # Deploy to production
    result = run('vercel --prod --yes')
    if result.returncode == 0:
        log('Deploy successful!')
        return True
    return False

def deploy_netlify():
    """通过Netlify CLI部署"""
    log('Deploying to Netlify...')
    result = run('netlify deploy --prod --dir=.')
    if result.returncode == 0:
        log('Deploy successful!')
        return True
    return False

def start_dev_server(port=8080):
    """启动本地开发服务器"""
    log(f'Starting dev server on http://localhost:{port}')
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(('127.0.0.1', port), handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    log(f'Dev server running at http://localhost:{port}')
    return server

def add_tool(name, description, html_code):
    """添加新工具到网站"""
    log(f'Adding new tool: {name}')
    index_path = os.path.join(PROJECT_DIR, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # This is a simplified version - full implementation would inject the tool
    # into the tools-grid and create a new tool-panel
    log(f'Tool "{name}" code ready for insertion')
    log(f'Description: {description}')
    return True

def update_seo(title=None, description=None, keywords=None):
    """更新SEO元数据"""
    index_path = os.path.join(PROJECT_DIR, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    if title:
        html = html.replace(
            '<title>DevTools Free - JSON格式化 / AI文案生成 / 图片去背景</title>',
            f'<title>{title}</title>'
        )
    if description:
        old_desc = '<meta name="description" content="'
        start = html.find(old_desc)
        if start >= 0:
            end = html.find('"', start + len(old_desc))
            html = html[:start] + old_desc + description + html[end:]

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    log('SEO updated')

def save_deploy_record(success, url=None):
    """记录部署历史"""
    record = {
        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'success': success,
        'url': url,
        'hash': hashlib.md5(open(os.path.join(PROJECT_DIR,'index.html'),'rb').read()).hexdigest()[:8]
    }
    records = []
    if os.path.exists(DEPLOY_LOG):
        records = json.loads(open(DEPLOY_LOG).read())
    records.append(record)
    open(DEPLOY_LOG, 'w').write(json.dumps(records, indent=2))
    log(f'Deploy record saved: {record["hash"]}')

def main():
    log('=== DevTools Auto Deploy ===')

    if '--setup' in sys.argv:
        log('First-time setup:')
        log('1. Register on vercel.com or netlify.com')
        log('2. Run: vercel login (or netlify login)')
        log('3. Run: python deploy.py')
        return

    # Verify local build
    if not verify_local():
        log('Local verification FAILED')
        sys.exit(1)

    log('Local verification PASSED')

    # Try Vercel first, then Netlify
    deployed = deploy_vercel()
    if not deployed:
        deployed = deploy_netlify()

    if deployed:
        save_deploy_record(True, 'https://devtools-free.vercel.app')
    else:
        log('Deployment failed. Check network and auth.')
        log('Run "vercel login" or "netlify login" first.')

if __name__ == '__main__':
    main()
