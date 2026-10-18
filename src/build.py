"""エクスネット コーポレートサイト（デザイン v0.1）を書き出す。
使い方：python3 build.py  →  ../site/ に HTML と site.css を出す。
原稿はこのファイルの中に直接書いている。色・余白はデザインシステム「エクスネット」のトークンだけを使う。
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'site')
os.makedirs(OUT, exist_ok=True)

# ---------- CSS：トークン → 部品（bundle.css）→ ページ組み（site.css） ----------
tokens = subprocess.run([sys.executable, os.path.join(HERE, 'tokens_css.py'), os.path.join(HERE, 'tokens.json')],
                        capture_output=True, text=True, check=True).stdout
bundle = open(os.path.join(HERE, 'bundle.css')).read()
site = open(os.path.join(HERE, 'site.css')).read()
import shutil
for _f in ('ikai.webp', 'ogp.png', 'favicon.svg', 'apple-touch-icon.png'): shutil.copy(os.path.join(HERE, _f), os.path.join(OUT, _f))
open(os.path.join(OUT, 'site.css'), 'w').write('/* tokens（tokens.json から生成） */\n' + tokens + '\n' + bundle + '\n' + site)

# ---------- 共通部品 ----------
ARROW = '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M0 5h12M8 1l4 4-4 4"/></svg>'
def logo(cid):
    # EXNET ロゴタイプ（案G、104×22、線の太さ2.8px。X の右上がりの線が交点で途切れ、2本の線が重なって走る形）
    import math
    w = 2.8; h = w / 2; t, b = 3 + h, 19 - h
    E = lambda x, ww=13: f'M{x+ww} {t}H{x+h}V{b}H{x+ww}M{x+h} 11H{x+ww-1.5}'
    X0, X1 = 21, 37; mx, my = (X0 + X1) / 2, 11; gap = 2.4
    L = math.hypot(X1 - X0, 18); ux, uy = (X1 - X0) / L, 18 / L
    ax, ay, cx, cy = mx + ux * gap, my - uy * gap, mx - ux * gap, my + uy * gap
    return (f'<svg class="logo" viewBox="0 0 104 22" width="104" height="22" role="img" aria-label="EXNET">'
            f'<defs><clipPath id="{cid}"><rect x="0" y="3" width="104" height="16"/></clipPath></defs>'
            f'<g fill="none" stroke="currentColor" stroke-width="{w}" clip-path="url(#{cid})">'
            f'<path d="{E(0)}"/><path d="M{X0} 2L{X1} 20"/><path d="M{X1} 2L{ax:.2f} {ay:.2f}M{cx:.2f} {cy:.2f}L{X0} 20"/>'
            f'<path d="M{45+h} 20V{t}L{60-h} {b}V2"/><path d="{E(68)}"/><path d="M89 {t}H104M96.5 {t}V20"/></g></svg>')

TOC_JS = "<script>\n(function(){var t=document.querySelector('.side-toc');if(!t)return;\nfunction chk(){var r=t.getBoundingClientRect(),hit=false;document.querySelectorAll('.ex-hero, .ex-fcta').forEach(function(n){var b=n.getBoundingClientRect();if(b.bottom>r.top&&b.top<r.bottom)hit=true;});t.classList.toggle('is-hidden',hit);}\nchk();addEventListener('scroll',chk,{passive:true});addEventListener('resize',chk);})();\n</script>"
def circle(): return f'<span class="ex-circle">{ARROW}</span>'
def more(label, href): return f'<a class="ex-more" href="{href}">{label}{circle()}</a>'
def btn(label, href, kind='primary', extra=''): return f'<a class="ex-btn ex-btn--{kind} {extra}" href="{href}">{label}<span class="ex-arrow">→</span></a>'

NAV = [('service', 'サービス', 'service.html'), ('case', '事例', 'case.html'), ('price', '料金と契約', 'price.html'),
       ('approach', '考え方', 'approach.html'), ('company', '会社情報', 'company.html')]
UTIL = [('コラム', 'column.html'), ('お知らせ', 'company.html#news'), ('代表メッセージ', 'message.html')]

def header(cur):
    nav = ''.join(f'<a class="ex-ul{" is-current" if k == cur else ""}" href="{h}">{l}</a>' for k, l, h in NAV)
    util = ''.join(f'<a class="ex-ul" href="{h}">{l}</a>' for l, h in UTIL)
    menu = ''.join(f'<li><a href="{h}">{l}<span>›</span></a></li>' for _, l, h in NAV + [(0, 'コラム', 'column.html'), (0, '代表メッセージ', 'message.html'), (0, 'PMVV', 'mission.html')])
    return f'''<div class="site-head">
<header class="ex-header"><div class="wrap--header">
<div class="ex-header__util">{util}</div>
<div class="ex-header__main"><span class="ex-header__logo"><a href="index.html" aria-label="エクスネット トップへ">{logo("lg-h")}</a></span>
<nav class="ex-header__nav" aria-label="メインメニュー">{nav}</nav>
<div class="ex-header__cta"><a class="ex-btn ex-btn--secondary ex-btn--header" href="download.html">資料請求</a><a class="ex-btn ex-btn--primary ex-btn--header" href="contact.html">無料相談</a></div></div>
</div></header>
<header class="ex-mhead"><span class="ex-mhead__logo"><a href="index.html" aria-label="エクスネット トップへ">{logo("lg-m")}</a></span><button class="ex-mhead__btn" id="menu-open" aria-label="メニューを開く" aria-controls="mmenu" aria-expanded="false"><i></i><i></i><i></i></button></header>
</div>
<div class="mmenu" id="mmenu" hidden><div class="ex-mmenu">
<div class="ex-mmenu__top"><span class="ex-mmenu__logo">{logo("lg-mm")}</span><button class="ex-mmenu__close" id="menu-close" aria-label="メニューを閉じる">×</button></div>
<ul>{menu}</ul>
<div class="ex-mmenu__cta"><a href="download.html">資料請求</a><a href="contact.html">無料相談（オンライン45分）</a></div>
</div></div>'''

FCTA_ITEMS = {
 'download': f'''<div><h3>資料請求</h3><p>進め方、2つの入り方、料金と契約の条件をまとめた資料をお送りします。</p><a class="ex-sqbtn" href="download.html">資料を受け取る{circle()}</a></div>''',
 'contact': f'''<div><h3>無料相談</h3><p>オンライン45分。いまのご商談のどこから手を付けるとよいかをお伝えします。</p><a class="ex-sqbtn" href="contact.html">相談を申し込む{circle()}</a></div>''',
 'note': f'''<div><h3>代表の実録</h3><p>代表の猪飼が、日々の支援で考えていることを note に書いています。</p><a class="ex-sqbtn" href="https://note.com/exnet" target="_blank" rel="noopener">note を読む{circle()}</a></div>''',
}
def foot_cta(skip=None):
    items = [v for k, v in FCTA_ITEMS.items() if k != skip]
    cls = 'ex-fcta' if len(items) == 3 else 'ex-fcta ex-fcta--2'
    return f'<section class="{cls}" aria-label="お問い合わせ">\n' + '\n'.join(items) + '\n</section>'
FOOT_CTA = foot_cta()

FOOTER = f'''<footer class="foot"><div class="wrap wrap--foot">
<div class="foot__in">
<div><div class="foot__logo">{logo("lg-f")}</div><p class="foot__addr">株式会社エクスネット<br>〒102-0083 東京都千代田区麹町1-4-4 ZENITAKA ANNEX 2F<br>03-6262-1694</p></div>
<div class="foot__map">
<div><h4>サービス</h4><ul><li><a class="ex-ul" href="service.html">サービス</a></li><li><a class="ex-ul" href="case.html">事例</a></li><li><a class="ex-ul" href="price.html">料金と契約</a></li><li><a class="ex-ul" href="approach.html">考え方</a></li><li><a class="ex-ul" href="column.html">コラム</a></li></ul></div>
<div><h4>会社情報</h4><ul><li><a class="ex-ul" href="company.html">会社概要</a></li><li><a class="ex-ul" href="message.html">代表メッセージ</a></li><li><a class="ex-ul" href="mission.html">PMVV</a></li><li><a class="ex-ul" href="company.html#news">お知らせ</a></li></ul></div>
<div><h4>お問い合わせ</h4><ul><li><a class="ex-ul" href="download.html">資料請求</a></li><li><a class="ex-ul" href="contact.html">無料相談</a></li></ul></div>
</div></div>
<div class="foot__legal"><a class="ex-ul" href="privacy.html">プライバシーポリシー</a><span>© Exnet Co., Ltd.</span></div>
</div></footer>
<a class="to-top" href="#top" aria-label="ページの先頭へ">{ARROW}</a>'''

MENU_JS = '''<script>
(function(){var m=document.getElementById('mmenu'),o=document.getElementById('menu-open'),c=document.getElementById('menu-close');
if(!m||!o)return;function s(v){m.hidden=!v;o.setAttribute('aria-expanded',v?'true':'false');document.body.style.overflow=v?'hidden':'';if(v)c.focus();else o.focus();}
o.addEventListener('click',function(){s(true)});c.addEventListener('click',function(){s(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden)s(false)});})();
</script>'''

TOP_JS = """<script>
(function(){try{history.scrollRestoration='manual'}catch(e){}
var moved=false;['wheel','touchstart','keydown','mousedown'].forEach(function(ev){addEventListener(ev,function(){moved=true},{passive:true,once:true})});
function go(){if(moved)return;var h=location.hash.slice(1),el=h&&h!=='top'&&document.getElementById(h);
if(el){el.scrollIntoView({block:'start',behavior:'instant'});return;}
window.scrollTo({top:0,left:0,behavior:'instant'});var t=document.getElementById('top')||document.body.firstElementChild;if(t&&t.scrollIntoView)t.scrollIntoView({block:'start',behavior:'instant'});}
go();
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);
addEventListener('load',function(){go();[150,400,900,1600].forEach(function(ms){setTimeout(go,ms)});});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(go);
if(window.ResizeObserver){var n=0,ro=new ResizeObserver(function(){if(++n>20||moved){ro.disconnect();return;}go();});ro.observe(document.body);setTimeout(function(){ro.disconnect()},3000);}
addEventListener('pageshow',function(e){if(e.persisted){moved=false;go();}});})();
</script>"""

# ---------- 検索・AI向けの情報（説明文、OGP、構造化データ、サイトマップ） ----------
import json, re, datetime, glob
BASE = 'https://exnet.biz/'
SITE_NAME = '株式会社エクスネット'
SEO = {'crumbs': None, 'faqs': []}
PAGES = []   # サイトマップに載せるページ
COLUMNS = {}  # コラム記事（column-*.html）。記事ごとに下で登録する
DESC = {
    'index.html': '株式会社エクスネットは、面談で販売する高単価の商品・サービスを、商談までの流れの仕組み化とテクノロジーで伸ばすマーケティング会社です。2011年創業。広告の成果は、面談のあとで決まります。だから広告を増やす前に、いまある面談で決まる件数から見直します。',
    'service.html': '面談で販売する高単価の商品・サービスを扱う事業者向けの伴走支援です。伴走型と伴走＋実務型の2つの入り方、支援の進め方、最初の2週間でお渡しするものをご紹介します。',
    'price.html': 'エクスネットの伴走支援の料金と契約条件です。月額、増えた売上にだけいただく成果報酬、契約期間、広告代理店の手数料との違いをまとめています。',
    'approach.html': '広告より先に商談を見る。エクスネットが、高単価の商品・サービスの売上を伸ばすときに、商談と導線のどこから手を付けるかという考え方をお伝えします。',
    'company.html': '株式会社エクスネットの会社概要と沿革、代表のご紹介です。2011年に名古屋で創業し、現在は東京都千代田区麹町に本社を置いています。',
    'mission.html': '株式会社エクスネットのパーパス、ミッション、ビジョン、バリュー（PMVV）です。',
    'message.html': '株式会社エクスネット代表取締役 猪飼智弘のメッセージです。広告より先に商談を見ると決めた理由を、自分の事業での失敗からお話しします。',
    'case.html': 'エクスネットのお客様の事例と、弊社自身の営業の数字です。面談に来てくださった割合など、商談側の数字を中心に掲載しています。',
    'case-edu.html': '高単価の教育サービスの事例です。6ヶ月のご支援で、予約した面談に来てくださる割合が31.3%から63.2%になり、売上は1,206万円になりました。',
    'case-exnet-btob.html': 'エクスネット自身の高単価サービスの数字です。2025年度、1つの商品で面談95件からご成約13件、売上1,602万円になった流れを公開しています。',
    'case-exnet-form-dm.html': 'エクスネット自身の営業の記録です。843通の問い合わせフォーム営業から、面談11件・ご成約2件につながった流れと数字を公開しています。',
    'download.html': 'エクスネットのサービス資料のご請求ページです。サイトでご紹介しているサービス内容を、図解入りの1冊にまとめたPDFを、メールですぐにお送りします。',
    'contact.html': 'エクスネットの無料相談（オンライン45分）のお申し込みページです。お名前などをご入力のうえ日時を選ぶと、その場で予約が確定します。',
    'privacy.html': '株式会社エクスネットのプライバシーポリシーです。',
}
ORG = {
    '@type': 'Organization', '@id': BASE + '#org', 'name': SITE_NAME, 'alternateName': ['エクスネット', 'Exnet Co., Ltd.'],
    'url': BASE, 'email': 'info@exnet.biz', 'foundingDate': '2011-06',
    'description': DESC['index.html'],
    'address': {'@type': 'PostalAddress', 'postalCode': '102-0083', 'addressRegion': '東京都', 'addressLocality': '千代田区',
                'streetAddress': '麹町1-4-4 ZENITAKA ANNEX 2F', 'addressCountry': 'JP'},
    'founder': {'@id': BASE + 'message.html#ikai'},
}
PERSON = {'@type': 'Person', '@id': BASE + 'message.html#ikai', 'name': '猪飼 智弘', 'alternateName': 'Tomohiro Ikai',
          'jobTitle': '代表取締役', 'worksFor': {'@id': BASE + '#org'}, 'image': BASE + 'ikai.webp', 'url': BASE + 'message.html'}

def strip_tags(t): return re.sub(r'<[^>]+>', '', t).strip()

def seo_head(fname, title, noindex):
    url = BASE + ('' if fname == 'index.html' else fname)
    desc = DESC.get(fname, '')
    out = []
    if desc: out.append(f'<meta name="description" content="{desc}">')
    if noindex: out.append('<meta name="robots" content="noindex">')
    out += [f'<link rel="canonical" href="{url}">',
            f'<meta property="og:title" content="{title}">', f'<meta property="og:description" content="{desc}">',
            f'<meta property="og:url" content="{url}">', f'<meta property="og:type" content="{"website" if fname == "index.html" else "article"}">',
            f'<meta property="og:site_name" content="{SITE_NAME}">', '<meta property="og:locale" content="ja_JP">',
            f'<meta property="og:image" content="{BASE}ogp.png">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">', '<meta name="twitter:card" content="summary_large_image">']
    graph = []
    if fname == 'index.html':
        graph += [ORG, PERSON, {'@type': 'WebSite', '@id': BASE + '#site', 'url': BASE, 'name': SITE_NAME, 'inLanguage': 'ja', 'publisher': {'@id': BASE + '#org'}}]
    elif fname in ('company.html', 'message.html'):
        graph += [ORG, PERSON]
    if fname == 'service.html':
        graph.append({'@type': 'Service', 'name': '伴走支援（伴走型／伴走＋実務型）', 'serviceType': 'マーケティング支援',
                      'provider': {'@id': BASE + '#org'}, 'areaServed': 'JP', 'description': DESC['service.html'], 'url': url})
    if fname in COLUMNS:
        c = COLUMNS[fname]
        graph += [ORG, PERSON]
        graph.append({'@type': 'Article', 'headline': c['title'], 'description': desc, 'datePublished': c['date'], 'dateModified': c['date'],
                      'author': {'@id': PERSON['@id']}, 'publisher': {'@id': BASE + '#org'}, 'image': BASE + 'ogp.png',
                      'mainEntityOfPage': url, 'inLanguage': 'ja'})
    if fname.startswith('case-'):   # 事例も記事として扱い、数字の出どころ（会社と代表）を結びつける
        graph += [ORG, PERSON]
        graph.append({'@type': 'Article', 'headline': title.rsplit('｜', 1)[0], 'description': desc, 'datePublished': '2026-10-17', 'dateModified': '2026-10-17',
                      'author': {'@id': PERSON['@id']}, 'publisher': {'@id': BASE + '#org'}, 'image': BASE + 'ogp.png',
                      'mainEntityOfPage': url, 'inLanguage': 'ja', 'articleSection': '事例'})
    if SEO['crumbs']:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': strip_tags(l), **({'item': BASE + ('' if h == 'index.html' else h)} if h else {'item': url})}
            for i, (l, h) in enumerate(SEO['crumbs'])]})
    if SEO['faqs']:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': strip_tags(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in SEO['faqs']]})
    if graph:
        out.append('<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>')
    SEO['crumbs'], SEO['faqs'] = None, []
    if not noindex: PAGES.append(url)
    return '\n'.join(out)

# 検索結果に出るタイトル。お客さんが検索する言葉（高単価・個別相談・成約率・成果報酬）を入れる
TITLES = {
    'service.html': '高単価の商品・サービスの成約率を上げる、商談から入る伴走支援',
    'price.html': '料金と契約｜月額＋成果報酬型のマーケティング支援',
    'approach.html': '考え方｜高単価の商品・サービスは、広告より先に個別相談・商談から',
    'case.html': '事例｜高単価の商品・サービスで、面談と成約が増えた記録',
    'case-edu.html': '面談に来てくださる割合が倍に｜高単価の教育サービスの事例',
    'case-exnet-btob.html': '面談95件からご成約13件・売上1,602万円｜高単価サービスの事例',
    'case-exnet-form-dm.html': '問い合わせフォーム営業の効果｜843通から面談11件・ご成約2件',
}

GA4_ID = 'G-6TWGWMNKEK'          # GA4 プロパティ「exnet.biz コーポレートサイト」
CLARITY_ID = 'yz19bttupo'        # Clarity プロジェクト「exnet.biz コーポレートサイト」
def analytics(fname):
    lead = {'thanks-download.html': 'download', 'thanks-contact.html': 'contact'}.get(fname)
    ev = f"gtag('event','generate_lead',{{form:'{lead}'}});" if lead else ''
    return (f'\n<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>'
            f"\n<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4_ID}');{ev}</script>"
            f'\n<script>(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{CLARITY_ID}");</script>')

def doc(fname, title, body, cur=None, lp=False, extra_js='', fcta_skip=None):
    full_title = 'エクスネット｜面談で売る高単価の商品・サービスを伸ばすマーケティング会社' if fname == 'index.html' else f'{TITLES.get(fname, title)}｜{SITE_NAME}'
    head = (f'<title>{full_title}</title>\n' + seo_head(fname, full_title, fname.startswith(('thanks-', 'test-')) or fname == '404.html') +
            '\n<meta name="claude:viewport-fit-sides" content="cover">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="stylesheet" href="site.css">')
    if not os.environ.get('SITE_ARTIFACT'): head += analytics(fname)   # プレビューでは計測しない
    if lp:
        inner = f'<div class="ex-root" id="top"><header class="lp-head"><span class="ex-header__logo"><a href="index.html" aria-label="エクスネット トップへ">{logo("lg-lp")}</a></span></header>\n<main>{body}</main>\n<footer class="lp-foot">© Exnet Co., Ltd.</footer></div>{TOP_JS}{extra_js}'
    else:
        inner = f'<div class="ex-root" id="top">{header(cur)}\n<main>{body}</main>\n{foot_cta(fcta_skip)}\n{FOOTER}</div>{TOP_JS}{MENU_JS}{extra_js}'
    if fname == 'index.html' and os.environ.get('SITE_ARTIFACT'):   # Artifact 公開用：doctype などは公開時に付く
        html = head + '\n' + inner
    else:
        html = f'<!doctype html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head><body>\n{inner}\n</body></html>'
    open(os.path.join(OUT, fname), 'w').write(html)

def crumb(items, navy=False):
    SEO['crumbs'] = items
    li = ''.join(f'<li><a href="{h}">{l}</a></li>' if h else f'<li>{l}</li>' for l, h in items)
    return f'<ol class="ex-crumb{" ex-crumb--on-navy" if navy else ""}" aria-label="パンくずリスト">{li}</ol>'

def hero(items, h1, lead, buttons=True):
    b = ('<div class="ex-hero__cta"><a class="ex-btn ex-btn--on-navy" href="download.html">資料請求<span class="ex-arrow">→</span></a>'
         '<a class="ex-btn ex-btn--on-navy-fill" href="contact.html">無料相談<span class="ex-arrow">→</span></a></div>') if buttons else ''
    return f'<section class="ex-hero"><div class="wrap--header">{crumb(items, True)}<div class="ex-hero__body"><h1>{h1}</h1><p>{lead}</p>{b}</div></div></section>'

def phead(items, label, h1, lead, buttons=True):
    b = ('<div class="ex-phead__cta"><a class="ex-btn ex-btn--secondary" href="download.html">資料請求<span class="ex-arrow">→</span></a>'
         '<a class="ex-btn ex-btn--primary" href="contact.html">無料相談<span class="ex-arrow">→</span></a></div>') if buttons else ''
    return f'<section class="ex-phead"><div class="wrap--header">{crumb(items)}</div><div class="ex-phead__body"><div class="ex-phead__label">{label}</div><h1>{h1}</h1><p>{lead}</p>{b}</div></section>'

def rule(t, left=False): return f'<h2 class="ex-ctitle ex-ctitle--rule{" ex-ctitle--left" if left else ""}"><span>{t}</span></h2>'
def dash(t, left=False): return f'<h2 class="ex-ctitle ex-ctitle--dash{" ex-ctitle--left" if left else ""}"><span>{t}</span></h2>'
def numh(n, sub, title, tag='h3'):
    return f'<div class="ex-numh"><span class="ex-numh__num">{n}</span><div><div class="ex-numh__sub">{sub}</div><{tag} class="ex-numh__title">{title}</{tag}></div></div>'
def ov_table(rows):
    seen, out = set(), []
    for k, v in rows:
        if k in seen: continue
        seen.add(k); out.append(f'<tr><th>{k}</th><td>{v}</td></tr>')
    return '<table class="tbl-ov"><tbody>' + ''.join(out) + '</tbody></table>'

def faq(items):
    SEO['faqs'] += items
    return '<div class="ex-faq">' + ''.join(
        f'<div class="ex-faq__item"><div class="ex-faq__q"><span class="ex-faq__badge">Q</span><p>{q}</p></div>'
        f'<div class="ex-faq__a"><span class="ex-faq__badge">A</span><p>{a}</p></div></div>' for q, a in items) + '</div>'
def ph(label, cls=''): return f'<div class="ph {cls}" role="img" aria-label="{label}（仮）">{label}<br>（写真が届いたら差し替え）</div>'
def photo(cap=True):
    fc = '<figcaption><b>TOMOHIRO IKAI</b>代表取締役 猪飼 智弘</figcaption>' if cap else ''
    return f'<figure class="portrait"><span class="portrait__frame"><img src="ikai.webp" alt="代表取締役 猪飼 智弘" width="330" height="330"></span>{fc}</figure>'

# ---------- 写真の代わりの図版（線と数字だけで描く。中身はすべて原稿にある事実） ----------
def fig_order(cls=''):
    st = [('01', 'ご商談の改善', 'すぐ〜1ヶ月'), ('02', '受け皿の設置', 'その日から蓄積'), ('03', 'ハウスリストの活用', 'リストが育ってから'), ('04', '広告でリードを足す', '1〜3ヶ月')]
    items = ''.join(f'<li class="{"is-first" if i == 0 else ""}"><span class="fig-order__n">{n}</span><b>{t}</b><small>{w}</small></li>' for i, (n, t, w) in enumerate(st))
    return f'<figure class="fig fig-order {cls}" aria-label="手を入れる順番"><figcaption class="fig__cap">手を入れる順番</figcaption><ol>{items}</ol><p class="fig__foot">広告は最後。先に、いまある面談で決まる件数を増やします。</p></figure>'
def fig_same():
    return ('<figure class="fig fig-same" aria-label="同じ広告費、同じ面談の数でも"><figcaption class="fig__cap">変えるのは、ここだけ</figcaption>'
            '<dl><div><dt>広告費</dt><dd>同じ</dd></div><div><dt>面談の数</dt><dd>同じ</dd></div><div class="is-key"><dt>決まる件数</dt><dd>増やす</dd></div></dl></figure>')
def fig_fee():
    return ('<figure class="fig fig-fee" aria-label="成果報酬の率"><figcaption class="fig__cap">その月に増えた売上に対する率</figcaption>'
            '<ul><li style="--h:100%"><span class="fig-fee__bar"></span><b>20%</b><small>300万円まで</small></li>'
            '<li style="--h:50%"><span class="fig-fee__bar"></span><b>10%</b><small>300万〜1,000万円の部分</small></li>'
            '<li style="--h:25%"><span class="fig-fee__bar"></span><b>5%</b><small>それを超える部分</small></li></ul>'
            '<p class="fig__foot">増えた売上が大きくなるほど、率は下がります。</p></figure>')
def fig_record(title='毎週の記録'):
    rows = [('仮説', ''), ('試したこと', ''), ('数字', ''), ('分かったこと', ''), ('次にやること', ''), ('お約束の状況', '')]
    return (f'<figure class="fig fig-record" aria-label="{title}"><figcaption class="fig__cap">{title}<span>第◯週</span></figcaption>'
            + '<dl>' + ''.join(f'<div><dt>{r}</dt><dd><i></i><i></i></dd></div>' for r, _ in rows) + '</dl></figure>')
def fig_funnel(st=None, label='843通から2件のご成約まで'):
    st = st or [('843', '通', '送付'), ('27', '件', '資料請求'), ('11', '件', '面談'), ('2', '件', 'ご成約')]
    return (f'<figure class="fig fig-funnel" aria-label="{label}"><ol style="grid-template-columns:repeat({len(st)},1fr)">'
            + ''.join(f'<li><b>{n}<small>{u}</small></b><span>{l}</span></li>' for n, u, l in st) + '</ol></figure>')
def fig_change(before, after, unit, label):
    return (f'<figure class="fig fig-change" aria-label="{label} {before}{unit}から{after}{unit}へ"><div class="fig-change__row">'
            f'<div><b>{before}<small>{unit}</small></b><span>開始時</span></div><i aria-hidden="true">→</i>'
            f'<div class="is-after"><b>{after}<small>{unit}</small></b><span>期間中</span></div></div><p class="fig__foot">{label}</p></figure>')
FUN_BTOB = [('125', '件', '面談の予約'), ('95', '件', '面談'), ('13', '件', 'ご成約')]

def dlbar():
    return ('<div class="ex-dlbar"><div><h3>サービスの内容と料金を、資料でご覧いただけます</h3><p>進め方、2つの入り方、料金と契約の条件をまとめています。</p></div>'
            '<a class="ex-btn ex-btn--primary" href="download.html">資料をダウンロード<span class="ex-arrow">→</span></a></div>')

REP_BIO = '''<ul>
<li>2011年、名古屋でウェブ制作会社として株式会社エクスネットを創業</li>
<li>2023年、本社を東京都千代田区麹町へ移転</li>
<li>自社講座の販売、パートナーと物販講座の集客と運営に携わる</li>
<li>講座・スクール、コンサルティング、士業など、面談で販売する高単価の商品・サービスを中心に支援</li>
</ul>'''

SYSTEMS = [('自動請求', '月次の請求と決済を自動で行う'), ('広告の事前審査', '広告を出す前に、表現や規約に触れる箇所がないかを確かめる'),
           ('発信の自動化', 'X と note への投稿を、品質の確認をはさんで自動で行う'), ('営業の文面づくり', '相手の状況に合わせた営業の文面を下書きする'),
           ('全体の監視', '上の仕組みが止まっていないかを見張り、止まったら直す')]

# ====================================================================
# トップ
# ====================================================================
top = f'''
<section class="fv">
<div class="fv2 wrap wrap--fv">
<div class="fv2__main">
<p class="fv2__voice">株式会社エクスネット</p>
<h1 class="fv2__title">価値ある挑戦を<br>必要な人に届けるために</h1>
<p class="fv2__lead"><span>2011年創業</span><br><span>面談で販売する高単価の商品・サービスを、</span><br class="pc"><span>商談までの流れの仕組み化と</span><span>テクノロジーで伸ばす、マーケティング会社</span></p>
<div class="fv2__cta"><a class="ex-btn ex-btn--secondary ex-btn--section" href="download.html">資料請求<span class="ex-arrow">→</span></a><a class="ex-btn ex-btn--primary ex-btn--section" href="contact.html">無料相談（45分）<span class="ex-arrow">→</span></a></div>
</div>
<aside class="fv2__who" aria-label="伴走する人">
<div class="fv2__who-head">{photo(False)}<div><div class="rep__roman">TOMOHIRO IKAI</div><div class="rep__title">代表取締役／商談の伴走者</div><p class="rep__name">猪飼 智弘</p></div></div>
<p class="fv2__word">「私自身、講座や<span>コンサルティングを、</span><span>ウェブから</span><span>商談につなげて</span><span>売ってきました。</span><span>だから最初に、</span><span>御社の商談と、</span><span>そこに至る流れを</span><span>拝見します。」</span></p>
{more('代表メッセージを読む', 'message.html')}
</aside>
</div>
<div class="fv__band"><div class="wrap wrap--fv"><nav class="entry" aria-label="入口">
<a href="service.html"><div class="entry__head"><h2>サービス</h2>{circle()}</div><p>商談の改善から入り、受け皿、リスト、広告の順に進めます</p></a>
<a href="approach.html"><div class="entry__head"><h2>考え方</h2>{circle()}</div><p>広告より先に商談を見る理由と、料金をこの形にした理由</p></a>
<a href="price.html"><div class="entry__head"><h2>料金と契約</h2>{circle()}</div><p>月額と成果報酬、契約の条件をすべて載せています</p></a>
</nav></div></div>
<div class="fv__band-low"></div>
</section>

<section class="sec"><div class="wrap">
<div class="ex-heading"><p class="sec-voice"><span>「面談はあるのに、</span><span>決まる件数が安定しない」</span></p><h2>広告の成果は、<br>面談のあとで決まる。</h2><p><span>だから弊社は、</span><span>広告を増やす前に、</span><span>いまある面談で決まる件数から見直します。</span><br><span>弊社の商品は、</span><span>すでにある面談で</span><span>決まる件数を増やし、</span><span>そのやり方を御社に残す、</span><br class="pc"><span>マーケティングの</span><span>伴走支援ひとつです。</span><br><span>違いは、</span><span>日々の実務を誰が担うかだけです。</span></p></div>
<div class="panels">
<a class="ex-panel" href="service.html#ways"><div class="ex-panel__head"><h3>伴走型</h3>{circle()}</div>
<dl><dt>役割</dt><dd>実務は御社のご担当者様。弊社は設計と数字の判断を担います</dd><dt>向いている</dt><dd>社内にやり方を残したい会社</dd></dl>
</a>
<a class="ex-panel" href="service.html#ways"><div class="ex-panel__head"><h3>伴走＋実務型</h3>{circle()}</div>
<dl><dt>役割</dt><dd>実務まで弊社が担います。数字の判断は代表の猪飼が担い、最終の決定は御社にお願いします</dd><dt>向いている</dt><dd>社内に手を動かせる人がいない会社</dd></dl>
</a>
</div>
<p class="panel-note note">料金と契約の条件は、すべて公開しています。<a class="ex-ul" href="price.html">料金と契約を見る</a></p>
<div class="btn-row">{btn('サービスを見る', 'service.html', 'primary', 'ex-btn--section')}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="ex-heading"><h2>事例</h2><p>お客様の支援と、弊社自身の営業の数字です。<br>数字は実数を、期間とあわせて載せています。</p></div>
<div class="stats stat-box">
<a class="ex-stat" href="case-edu.html">
<div class="ex-stat__label">広告費に対する売上</div>
<div class="ex-stat__value"><span class="ex-stat__unit">約</span><span class="ex-stat__num">5</span><span class="ex-stat__unit">倍</span></div>
<div class="ex-stat__note">開始時90%→期間中466%。高単価の教育サービス（6ヶ月）</div></a>
<a class="ex-stat" href="case-exnet-btob.html">
<div class="ex-stat__label">面談95件から生まれた売上</div>
<div class="ex-stat__value"><span class="ex-stat__num">1,602</span><span class="ex-stat__unit">万円</span></div>
<div class="ex-stat__note">ご成約13件。弊社自身の高単価サービス（2025年度、1商材）</div></a>
</div>
<div class="btn-row">{btn('事例を見る', 'case.html', 'secondary', 'ex-btn--section')}</div>
</div></section>

<section class="sec--lg bg-alt"><div class="wrap">
<div class="ex-heading"><h2>エクスネットの特長</h2></div>
<div class="features">
<div class="ex-feature"><div class="ex-feature__num">01</div><div class="ex-feature__text">すでにある商談から入る</div>
<p>最初の2週間で、いまのご商談のどこで止まっているかを拝見します。改善点は3つまでに絞り、書面でお渡しします。</p>{more('進め方を見る', 'service.html#flow')}</div>
<div class="ex-feature"><div class="ex-feature__num">02</div><div class="ex-feature__text">増えた売上からだけ、<br>成果報酬をいただく</div>
<p>月々の費用のほかにいただくのは、弊社が担当した経路から生まれた売上に対する成果報酬だけです。広告費の額は、弊社の売上に関係しません。</p>{more('料金と契約を見る', 'price.html')}</div>
<div class="ex-feature"><div class="ex-feature__num">03</div><div class="ex-feature__text">やり方が御社に残る</div>
<p>毎週、何を試し、何が分かったかを記録に残します。残るのは操作の手順ではなく、判断の基準です。</p>{more('考え方を見る', 'approach.html')}</div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="ex-heading"><h2>代表</h2></div>
<div class="rep">
{photo(False)}
<div><div class="rep__roman">TOMOHIRO IKAI</div><div class="rep__title">代表取締役／商談の伴走者</div><p class="rep__name">猪飼 智弘</p>
{REP_BIO}
{more('代表メッセージを読む', 'message.html')}</div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="ex-heading"><h2>会社情報</h2></div>
<div class="rows rows--grid">
<a class="ex-row" href="company.html"><span>会社概要</span>{circle()}</a><a class="ex-row" href="message.html"><span>代表メッセージ</span>{circle()}</a>
<a class="ex-row" href="mission.html"><span>PMVV</span>{circle()}</a><a class="ex-row" href="company.html#news"><span>お知らせ</span>{circle()}</a>
</div></div></section>
'''
doc('index.html', '', top)

# ====================================================================
# サービス
# ====================================================================
steps = [('01', 'ご商談の改善', 'すでにあるご面談の成約率を上げます。', 'すぐ〜1ヶ月', 'なし'),
         ('02', '受け皿の設置', 'いまの導線に、LINE登録などを1ステップ挟みます。これから入るリードが、御社のリストとして貯まり始めます。', 'その日から蓄積', 'なし（LP・UTAGEの新規構築が必要な場合は別途お見積り）'),
         ('03', 'ハウスリストの活用', '貯まったリストや、これまでに失注したお客様に、個別に働きかけます。1回だけのチャンスで終わりにしません。', 'リストが育ってから', 'なし'),
         ('04', '広告によるリード追加', '広告で、面談の数そのものを増やします。流れが整ってから広告費を増やすので、成果が崩れにくくなります。', '1〜3ヶ月', '広告費（御社のご負担）')]
svc_faq = [
 ('依頼してから始めるまで、どのくらいかかりますか。', 'ご契約後、最初の2週間でご商談の確認と設計を行い、1ヶ月目から実施します。LPやUTAGEを新しく作る場合は、その制作期間が加わります。'),
 ('最初の2週間で、何をもらえますか。', '3つあります。現在のご商談（録画・トークスクリプト・資料のいずれか）を拝見してお渡しする、改善点3つまでの書面。受け皿（LINE登録など）の設計。そして、成果報酬の対象になる経路（弊社が担当する経路）と直近3ヶ月の数字を、一緒に確かめた記録です。'),
 ('毎週の報告では、何を教えてもらえますか。', '毎週15分、オンラインでお会いして、仮説、試したこと、数字、分かったこと、次にやること、お約束の状況の6つをお伝えします。月末には代表の猪飼から30分、今月分かったこと、来月の最優先、続ける・変えるの判断をお伝えします。'),
 ('約束したことが間に合わないときは、どうなりますか。', '弊社がお約束したことは、期限と状況を毎週の報告に書きます。間に合わない・できないと分かった場合は、その時点でお知らせします。'),
 ('広告の予算が少なくても、引き受けてもらえますか。', 'はい。弊社はまず、すでにあるご商談の改善から入ります。広告を使わずに始める「ご商談から」の範囲もご用意しています。'),
 ('「ご商談から」と「集客から」は、何が違いますか。', 'どちらも、ご商談の改善・受け皿・ハウスリストの活用を含みます。「集客から」では、これに広告運用が加わり、広告費は御社のご負担です。弊社への月額は、どちらも同じです。'),
 ('複数の事業や商品を、同時にお願いできますか。', '同時には進めません。同時に進めると、どの施策が効いたのか分からなくなるためです。まず1つで数字をつくり、再現できることを確かめてから広げます。'),
 ('実際に手を動かすのは誰ですか。社員の方ですか、外部の方ですか。', '伴走型では、日々の実務は御社のご担当者様が行い、弊社は設計と判断を担います。伴走＋実務型では、弊社の実務担当者が日々の運用を担います。どちらの場合も、判断と月末のレビューは代表の猪飼が担当します。'),
 ('外部の方が作業する場合、品質はどう確かめていますか。', '毎週の報告で、実施したことと数字を御社と同じ形で確認します。判断が要る点は代表が引き取り、月末のレビューで続ける・変えるを一緒に決めます。'),
 ('毎週の打ち合わせ以外に、チャットで相談できますか。', 'できます。'),
 ('どんな業種の実績がありますか。', 'スクール・講座、コンサルティング、士業など、面談で販売する高単価の商品・サービスが中心です。'),
 ('どんな会社が向いていますか。', '面談で販売している、単価の高い商品・サービスをお持ちの会社です。すでに広告やLINEなどの導線があり、意思決定をされる方と直接やり取りできることを前提にしています。')]
service = f'''
{hero([('ホーム', 'index.html'), ('サービス', None)], '個別相談・商談の成約率から上げる、<br class="pc">マーケティングの伴走支援',
      '広告の成果は、面談のあとで決まります。だから広告を増やす前に、いまある面談で決まる件数から見直します。<br class="pc">受け皿、リスト、広告の順に御社のご担当者様と一緒に進め、そのやり方を御社の中に残します。')}
<section class="sec bg-alt"><div class="wrap">
{dash('集客の前に、<br>いまある商談を見直します')}
<div class="wrap--article prose" style="margin:0 auto;padding:0">
<p>すでに月に何件もの面談があるなら、広告を増やすより先に、その面談で決まる件数を増やすほうが売上は早く動きます。だから最初に、いまある商談を一緒に見直します。そのうえで受け皿をつくり、貯まったリストに働きかけ、最後に広告で面談の数そのものを増やします。</p>
</div></div></section>

<section class="sec" id="issues"><div class="wrap">
{rule('こんなことは、ありませんか')}
<ul class="issues" style="border:1px solid var(--line)">
<li>面談はあるのに、決まる件数が安定しない</li><li>広告の運用者が、手前の獲得単価しか見てくれない</li>
<li>失注したお客様に、その後なにもできていない</li><li>集客が紹介や一つのプラットフォーム頼みで、止まったら終わってしまう</li>
</ul>
<p class="issues-note note">※実際の商談で伺った言葉をもとにしています</p>
<div class="tri" aria-hidden="true"></div>
{dash('この順番で、一つずつ解いていきます')}
</div></section>

<section class="sec bg-alt" id="steps"><div class="wrap">
{rule('4つの打ち手を、この順番で')}
<p class="lead-c">目指すのは、決まる件数が増え、そのやり方が御社に残る状態です。</p>
<div class="steps mt-40">{''.join(f'<div class="step">{numh(n, "打ち手 " + n, t)}<p>{d}</p><div class="meta"><span><b>効き始めるまで</b>　{w}</span></div></div>' for n, t, d, w, c in steps)}</div>
</div></section>

<section class="sec" id="ways"><div class="wrap">
{rule('入り方は2つあります')}
<p class="lead-c">違いは、日々の実務を誰が担うかです。どちらでも、設計と数字の判断は弊社が担います。</p>
<div class="tbl-wrap mt-40"><table class="tbl tbl--cmp">
<thead><tr><th></th><th>伴走型</th><th>伴走＋実務型</th></tr></thead><tbody>
<tr><th>実務をするのは</th><td>御社のご担当者様</td><td>弊社の実務担当者</td></tr>
<tr><th>弊社が担うこと</th><td>設計、数字の判断、改善のご提案</td><td>左に加えて、配信の修正、シナリオの差し替え、広告の運用と入稿</td></tr>
<tr><th>月額（税込）</th><td class="num">44,000円</td><td class="num">99,000円</td></tr>
<tr><th>向いている会社</th><td>社内にやり方を残したい会社、手を動かせるご担当者を1名決められる会社</td><td>社内に手を動かせる人がいない会社、広告まで任せたい会社</td></tr>
</tbody></table></div>
<p class="note mt-24">広告を使わない「ご商談から」でも始められます。月額は同じです。</p>
<div class="mt-40">{more('料金と契約の詳細', 'price.html')}</div>
</div></section>

<section class="sec bg-alt" id="flow"><div class="wrap">
{rule('進め方')}
<div class="tbl-wrap"><table class="tbl tbl--wide">
<thead><tr><th>時期</th><th>段階</th><th>内容</th></tr></thead><tbody>
<tr><td class="num">〜2週</td><th>ご商談の確認と設計</th><td>現在のご商談を拝見し、改善点を洗い出します。受け皿も設計します</td></tr>
<tr><td class="num">1ヶ月目</td><th>1つで検証</th><td>商談の改善を実施し、受け皿を実装します。集客から始める場合は、ここから広告を開始します</td></tr>
<tr><td class="num">2〜3ヶ月目</td><th>運転と改善</th><td>成約率の推移を見ながら調整します。3ヶ月目の月末に、残りの3ヶ月で何を続け、何を変えるかを一緒に決めます</td></tr>
<tr><td class="num">4ヶ月目〜</td><th>横展開</th><td>他の事業・商品へ広げます。リストが育った段階で、掘り起こしを始めます</td></tr>
</tbody></table></div>
<p class="lead-c mt-40">毎週15分の報告と、月末に代表との30分のレビューがあります。</p>
<div class="mt-40">{fig_record('毎週の報告（見本）')}</div>
</div></section>

<section class="sec" id="faq"><div class="wrap wrap--article">
{rule('よくある質問')}
{faq(svc_faq)}
</div></section>

<section class="sec bg-alt"><div class="wrap">
{dash('まずは、いまのご商談を<br class="sp">拝見させてください')}
<div class="two">
<a href="download.html"><h3>資料請求</h3><p>サービスの内容と料金をまとめた資料をお送りします。</p>{more('資料を受け取る', 'download.html').replace('<a class="ex-more" href="download.html">', '<span class="ex-more">').replace('</a>', '</span>')}</a>
<a href="contact.html"><h3>無料相談</h3><p>いまのご商談と導線を拝見し、どこから手を付けるとよいかをお伝えします（オンライン45分）。</p>{more('相談を申し込む', 'contact.html').replace('<a class="ex-more" href="contact.html">', '<span class="ex-more">').replace('</a>', '</span>')}</a>
</div></div></section>

<aside class="side-toc" aria-label="このページの目次"><ol>
<li><a href="#issues">よくある課題</a></li><li><a href="#steps">打ち手</a></li><li><a href="#ways">2つの入り方</a></li>
<li><a href="#flow">進め方</a></li><li><a href="#faq">よくある質問</a></li></ol>
<a class="ex-btn ex-btn--primary" href="contact.html">無料相談<span class="ex-arrow">→</span></a></aside>
{TOC_JS}
'''
doc('service.html', 'サービス', service, 'service')

# ====================================================================
# 料金と契約
# ====================================================================
price_faq = [
 ('なぜ、月額と成果報酬の組み合わせなのですか。', '月額をいただくのは、受け皿づくりやハウスリストの育成のように、すぐには数字に表れない打ち手にも取り組むためです。成果報酬をいただくのは、御社の売上が伸びるほど弊社の売上も増える形にして、同じ側に立つためです。'),
 ('伴走＋実務型の99,000円は、どういう内訳ですか。', '運用費44,000円と実務費55,000円です。運用費は、設計、数字の判断、改善のご提案、毎週の報告、代表による月末のレビュー（30分）の分で、伴走型の月額と同じです。実務費は、弊社の実務担当者が日々の運用を担う作業の分です。'),
 ('月額の中には、どこまでの作業が含まれていますか。', '伴走型では、設計、数字の判断、改善のご提案、毎週の報告、代表による月末のレビュー（30分）が含まれます。原稿は最初の2ヶ月は弊社が用意し、3ヶ月目からは御社の原稿を添削します。公式LINEで面談につなぐ仕組みも含みます。伴走＋実務型では、これに日々の運用が加わります。配信の修正、シナリオの差し替え、広告の運用と入稿です。「ご商談から」「集客から」のどちらの範囲でも、月額は変わりません。'),
 ('伴走型と伴走＋実務型で、作業の量に上限はありますか。', '伴走型では、実務を担当する方を社内で1名お決めいただきます（お一人で事業をされている場合は社長ご自身）。弊社へのご依頼の作業が月4時間を超える場合は、伴走＋実務型をご提案します。伴走＋実務型の実務は月約15時間までで、範囲と上限はご契約の前に書面で決めます。上限を超える作業が必要な場合は、着手の前にお見積りし、ご了承をいただいてから進めます。'),
 ('成果報酬の料率は、売上が大きくなるとどう変わりますか。', '増えた売上が大きいほど、率は下がります。その月の対象売上のうち、300万円までは20%、300万円を超え1,000万円までの部分は10%、それを超える部分は5%です。対象売上が500万円の月は、300万円×20%＋200万円×10%＝80万円になります。'),
 ('売上がどのくらい増えれば、費用を払っても御社はプラスになりますか。', '増えた売上のうち8割は御社に残ります。月額を含めて手元がプラスになるのは、増えた売上が、伴走型で月55,000円、伴走＋実務型で月123,750円を超えたときです（月額÷0.8。増えた売上が300万円までの範囲）。商品の原価と広告費は含めていません。集客から始める場合は、広告費を加えた額が目安です。ご商談からの範囲では成果報酬が生じないため、増えた売上が月額を超えた時点でプラスです。'),
 ('「増えた売上」は、どうやって確かめますか。', '弊社が担当した経路から来たお客様のご成約かどうかで判定します。どの経路が弊社の担当かはご契約の前に書面で決め、毎月の成約数は、毎週の報告で御社と同じ数字を見ながら確認します。'),
 ('成果報酬は、税込と税抜のどちらで計算しますか。', '各月の税込売上で判定します（累計ではありません）。税込売上をもとに計算するため、計算した額に消費税を加算することはありません。'),
 ('「ご商談から」の範囲でも、成果報酬はかかりますか。', 'かかりません。既存の経路から来た面談で決まる件数が増えても、増えた分はすべて御社に残ります。成果報酬の対象は、弊社が始めた広告など、弊社が担当した経路からのご成約だけです。フォームDM経由の売上も対象外です。'),
 ('成果報酬を受け取れない業種（士業など）でも依頼できますか。', 'ご依頼いただけます。法令や業界の規程により成果報酬をお支払いいただけない業種の方には、成果報酬をいただかない形をご用意しています。内容と費用はご相談のうえで決めますので、無料相談でお聞かせください。'),
 ('広告費は誰が払いますか。弊社に預ける必要はありますか。', '広告費は御社から媒体へ直接お支払いいただき、広告アカウントも御社名義のまま運用します。弊社が広告費をお預かりしたり、立て替えたりすることはありません。'),
 ('広告代理店の「広告費の◯%」という手数料とは、何が違いますか。', '手数料の形では、広告費が増えるほど運用する側の売上が増えます。弊社は広告費の◯%をいただかないので、御社が広告費を増やしても弊社の取り分は増えません。弊社がいただくのは、弊社が担当した経路から生まれた売上に対する成果報酬です。決まる件数を増やすことが、弊社の売上につながります。'),
 ('契約期間はどのくらいですか。まず3ヶ月だけ試すことはできますか。', 'ご契約は6ヶ月からです。ご商談の改善は結果が表れるまでに2〜3ヶ月かかり、ハウスリストの活用はさらに時間がかかります。そのため3ヶ月目の月末に、残りの3ヶ月で何を続け、何を変えるかを一緒に決めます。6ヶ月の満了の前に、自社で進めるか、継続するかをお選びいただきます。'),
 ('伴走型から伴走＋実務型へ、途中で変えられますか。', '入り方の切り替えは、原則として6ヶ月の満了時に承ります。継続を選ばれるときに、入り方も選び直せます。'),
 ('LPやLINEの構築は月額に含まれますか。', '含まれません。LP制作やUTAGEの初期構築など、新たに作る作業は1件ごとにお見積りします。お見積りは制作費とディレクション費（完成イメージのすり合わせ・確認）を分けてお示しし、ご了承をいただいてから着手します。着手の前に、完成イメージに近い参考例を1つお送りください。修正は2回まで含み、3回目以降は改めてお見積りします。')]
price = f'''
{hero([('ホーム', 'index.html'), ('サービス', 'service.html'), ('料金と契約', None)], '料金と契約',
      'いただくのは、月額と、弊社が担当した経路から生まれた売上に対する成果報酬だけです。<br class="pc">設計費や着手金はいただきません。', False)}
<section class="sec bg-alt" id="monthly"><div class="wrap">
{rule('月額')}
<div class="tbl-wrap"><table class="tbl tbl--cmp">
<thead><tr><th></th><th>伴走型</th><th>伴走＋実務型</th></tr></thead><tbody>
<tr><th>月額（税込）</th><td class="num">44,000円</td><td class="num">99,000円</td></tr>
<tr><th>日々の実務をするのは</th><td>御社のご担当者様</td><td>弊社の実務担当者</td></tr>
<tr><th>原稿</th><td>最初の2ヶ月は弊社が用意し、3ヶ月目からは御社の原稿を添削</td><td>弊社が作成</td></tr>
<tr><th>広告の運用</th><td>御社が運用し、弊社が設計と数字の判断</td><td>弊社が運用（別料金なし）</td></tr>
<tr><th>公式LINEで面談につなぐ仕組み</th><td>含みます</td><td>含みます</td></tr>
<tr><th>毎週の報告と月末のレビュー（30分）</th><td>含みます</td><td>含みます</td></tr>
</tbody></table></div>
<ul class="list-dash note">
<li>伴走型は、社内で実務を担当する方を1名お決めいただきます。</li>
<li>広告費は、御社から媒体へ直接お支払いいただきます。</li>
</ul></div></section>

<section class="sec" id="fee"><div class="wrap">
{rule('成果報酬は、増えた売上にだけ')}
<p class="lead-c">弊社が担当した経路から生まれたご成約の売上に対して、毎月末日で締めて計算します。<br class="pc">対象売上が大きくなるほど、率が下がります。</p>
<div class="tbl-wrap tbl-wrap--article mt-40"><table class="tbl tbl--half">
<thead><tr><th>その月の対象売上</th><th>率</th></tr></thead><tbody>
<tr><th>300万円まで</th><td class="num">20%</td></tr>
<tr><th>300万円を超え、1,000万円までの部分</th><td class="num">10%</td></tr>
<tr><th>1,000万円を超える部分</th><td class="num">5%</td></tr>
</tbody></table></div>
<div class="box box--article mt-24"><h3>計算の例</h3><p>その月の対象売上が500万円の場合：<span class="calc">300万円×20%＋200万円×10%＝80万円</span></p></div>
<ul class="list-dash box--article mt-24" style="margin-left:auto;margin-right:auto">
<li>ご商談からの範囲ではかかりません。御社がもともとお持ちの経路からの売上は、増えた分もすべて御社に残ります。</li>
<li>対象のご成約がなければ、お支払いは月額だけです。</li>
</ul>
</div></section>

<section class="sec bg-alt" id="term"><div class="wrap">
{rule('ご契約の条件')}
<div class="tbl-wrap"><table class="tbl tbl--stack"><tbody>
<tr><th>ご契約期間</th><td>初回の契約期間は6ヶ月となり、自動更新はありません。満了の30日前までに、自社で進める（ご契約の終了）か継続をお選びいただきます。6ヶ月以上ご一緒したお客様は、顧問への移行もご相談いただけます。継続の場合は1ヶ月ごとのご契約で、30日前にお申し出いただければ終了できます</td></tr>
<tr><th>ご契約時のお支払い</th><td>月額の3ヶ月分（伴走型 <span class="num">132,000円</span>／伴走＋実務型 <span class="num">297,000円</span>）</td></tr>
<tr><th>4ヶ月目以降</th><td>毎月10日に、月額をお支払いいただきます（継続の場合も同じです）</td></tr>
<tr><th>成果報酬</th><td>毎月末日で締め、翌月にご請求します</td></tr>
<tr><th>お支払い方法</th><td>クレジットカード（ご契約時のお支払いは、銀行振込もお選びいただけます）</td></tr>
<tr><th>途中のご解約・値引き</th><td>6ヶ月の間の途中解約と、値引きはお受けしていません</td></tr>
</tbody></table></div>
<p class="note mt-24">このページの料金は、新しくご契約いただく場合のものです。すでにご契約中のお客様は、ご契約書の条件のままです。</p>
</div></section>

<section class="sec" id="faq"><div class="wrap wrap--article">
{rule('料金・契約についてよくある質問')}
{faq(price_faq)}
</div></section>
'''
doc('price.html', '料金と契約', price, 'price')

# ====================================================================
# 考え方
# ====================================================================
approach = f'''
{hero([('ホーム', 'index.html'), ('考え方', None)], '考え方',
      'なぜ商談から入るのか。なぜ増えた売上からだけ成果報酬をいただくのか。<br class="pc">ご契約の前に確かめておきたい「なぜ」を、ここにまとめました。')}
<section class="sec bg-alt"><div class="wrap"><div class="voice">
{dash('集客を<br>増やしても、<br>売上が安定しない', True)}
<div><p class="voice__q">「広告費も、外注先も変えてみた。それでも、勝ちパターンが見えない。」</p>
<div class="prose">
<p>面談で販売する高単価の商品・サービスでは、リードの数よりも、面談で決まるかどうかが売上を左右します。それでも多くの会社が、成果が出ないときに最初に手を入れるのは広告です。広告費を増やし、運用者を替え、それでも決まる件数が変わらない。</p>
<p>新しいお客様に目が行くのは、自然なことです。弊社の代表も、長くそうでした。新規を追いかけているほうが、仕事をしている実感があるからです。</p>
<p>弊社が最初に見直すのは、広告ではなく、手を入れる順番です。同じ広告費、同じ面談の数のままでも、決まる件数が変われば売上は変わります。</p>
</div></div></div></div></section>

<section class="sec"><div class="wrap">
{rule('高単価の商品・サービスで、<br class="sp">なぜ商談から入るのか')}
<div class="prose" style="max-width:var(--container-article);margin:0 auto">
<p>理由は3つあります。</p>
<p>1つ目は、止まらないからです。広告は、他社の規約ひとつで止まります。弊社自身、広告アカウントを2度止められました。面談で決まる件数を増やす仕事は、誰にも止められません。</p>
<p>2つ目は、お金がかからないからです。リードを増やす必要がなく、追加の費用もかかりません。すでにある面談の成約率が上がれば、それだけで売上が増えます。</p>
<p>3つ目は、広告が無駄にならないからです。広告の反応はよいのに売れない。これが、いちばんもったいない状態です。<b>決まる流れができる前に、広告費を増やすべきではありません。</b></p>
<p>ご商談の改善から始める場合、最初の2〜3ヶ月は、広告を回さなくても構いません。これまで決まらなかったお客様や、眠っているリストから掘り起こすほうが、早く数字が出ることも少なくありません。</p>
</div></div></section>

<section class="sec bg-alt"><div class="wrap">
<h2 class="ex-ctitle">弊社が一緒につくる、3つの状態</h2>
<div class="circles">
<div><b>決まる</b><span>すでにある面談で、<br>決まる件数が増える</span></div>
<div><b>貯まる</b><span>これから入るリードが、<br>御社のリストとして貯まる</span></div>
<div><b>残る</b><span>何を試し、何が分かったかが、<br>御社の中に残る</span></div>
</div></div></section>

<section class="sec--lg"><div class="wrap">
<div class="feat"><div class="feat__media">{fig_same()}</div><div>{numh('01', '特長①', 'すでにある商談から入る', 'h2')}
<div class="prose"><p>広告を増やす前に、いまある面談を見直します。最初の2週間で、現在のご商談（録画・トークスクリプト・資料のいずれか）を拝見し、改善点を3つまで書面でお渡しします。リードを増やさずに売上を変えられる余地が、まずそこにあることが多いからです。</p></div>
{more('サービスの進め方を見る', 'service.html#flow')}</div></div>
<div class="feat feat--rev"><div class="feat__media">{fig_fee()}</div><div>{numh('02', '特長②', '増えた売上からだけ、<br>成果報酬をいただく', 'h2')}
<div class="prose"><p>広告運用の対価を「広告費の◯%」でいただく形にすると、運用する側は「広告費を上げてください」としか言えなくなります。弊社がいただくのは、弊社が担当した経路から生まれた売上に対する成果報酬だけです。御社だけがリスクを取る形は、フェアではないと考えています。</p>
<p>一方で、完全な成果報酬にはしていません。そうすると、最短で数字が出る施策しか打てなくなり、リストの育成のように時間のかかる打ち手が後回しになるためです。月額の運用費は、その時間のかかる仕事にも取り組むためのものです。</p></div>
{more('料金と契約を見る', 'price.html')}</div></div>
<div class="feat"><div class="feat__media">{fig_record()}</div><div>{numh('03', '特長③', 'やり方が御社に残る', 'h2')}
<div class="prose"><p>弊社が抜けたあとに「何も残りませんでした、ゼロからやり直しです」となるのが、いちばんつらいことだと考えています。だから毎週、仮説を立て、試し、分かったことを記録に残します。</p>
<p>いずれ弊社がいなくても回る状態になれば、その時は離れていただいて構いません。それが、伴走という言葉の意味だと考えています。</p></div></div></div>
</div></section>

<section class="sec bg-alt"><div class="wrap">
{dash('毎週15分、オンラインでお会いします')}
<div class="prose" style="max-width:var(--container-article);margin:0 auto">
<p>どれだけ裏で手を動かしていても、伝わらなければ、御社から見れば何も進んでいないのと同じです。だから毎週15分、顔を合わせてお伝えします。</p>
<p>毎週の定例は、お互いに約束を守るための仕組みでもあります。</p>
</div></div></section>

<section class="sec" id="systems"><div class="wrap">
{rule('自社でも、同じことをしています')}
<p class="lead-c">弊社は、提案する仕組みを自社の事業でも使っています。以下は、弊社の業務で実際に稼働しているものです。ご提供する商品ではなく、弊社がこう働いている、という記録としてご覧ください。</p>
<div class="tbl-wrap mt-40"><table class="tbl tbl--stack"><tbody>{''.join(f'<tr><th>{n}</th><td>{d}</td></tr>' for n, d in SYSTEMS)}</tbody></table></div>
</div></section>

<section class="sec bg-alt"><div class="wrap">
{dash('複数の事業を、<br class="sp">同時には進めません')}
<div class="prose" style="max-width:var(--container-article);margin:0 auto">
<p>いくつもの事業や商品を同時に進めると、どの施策が効いたのか判別できなくなります。まず1つで数字をつくり、再現できることを確かめたうえで、ほかへ広げます。</p>
<p>想定どおりに運ばなかった場合も、1つであれば早い段階で気づき、止められます。</p>
</div></div></section>

<section class="sec"><div class="wrap">
{rule('代表')}
<div class="rep" style="margin-top:0">
{photo(False)}
<div><div class="rep__roman">TOMOHIRO IKAI</div><p class="rep__name">猪飼 智弘</p><div class="rep__title">株式会社エクスネット 代表取締役／商談の伴走者</div>
{REP_BIO}
<div class="ex-tags"><span class="ex-tag">#商談の改善</span><span class="ex-tag">#LINE導線</span><span class="ex-tag">#UTAGE</span><span class="ex-tag">#ハウスリスト</span><span class="ex-tag">#成果報酬</span></div>
{more('代表メッセージを読む', 'message.html')}</div></div>
</div></section>

<section class="sec bg-alt"><div class="wrap">{dlbar()}</div></section>
'''
doc('approach.html', '考え方', approach, 'approach')

# ====================================================================
# 会社情報
# ====================================================================
company = f'''
{phead([('ホーム', 'index.html'), ('会社情報', None)], 'COMPANY', '会社情報', '株式会社エクスネットの会社概要と、代表のご紹介です。')}
<section class="sec" style="padding-top:0"><div class="wrap">
{rule('会社概要', True)}
<dl class="ex-dl">
<dt>会社名</dt><dd>株式会社エクスネット（Exnet Co., Ltd.）</dd>
<dt>設立</dt><dd>2011年6月1日</dd>
<dt>所在地</dt><dd>〒102-0083 東京都千代田区麹町1-4-4 ZENITAKA ANNEX 2F</dd><dt>最寄り駅</dt><dd>東京メトロ半蔵門線 半蔵門駅から徒歩3分</dd>
<dt>代表者</dt><dd>代表取締役　猪飼 智弘</dd>
<dt>事業内容</dt><dd>マーケティングの伴走支援（商談の改善、LINE・UTAGEの導線設計、ハウスリストの活用、広告の運用）<br>自社システムの開発・運用</dd>
<dt>電話番号</dt><dd>03-6262-1694</dd>
<dt>メール</dt><dd><a class="ex-ul" href="mailto:info@exnet.biz">info@exnet.biz</a></dd>
<dt>沿革</dt><dd><ul class="hist"><li><span>2011年6月</span><span>名古屋でウェブ制作会社として創業</span></li><li><span>2012年5月</span><span>自社講座の販売を開始</span></li><li><span>2016年4月</span><span>自社システムの開発を始める</span></li><li><span>2018年8月</span><span>集客の仕組みづくりを自社で開始</span></li><li><span>2020年7月</span><span>パートナー会社と物販講座の運営を始める</span></li><li><span>2023年8月</span><span>本社を東京都千代田区麹町へ移転</span></li><li><span>2026年</span><span>伴走支援（伴走＋実務型）の提供を開始</span></li></ul></dd>
</dl>
<div class="map mt-64"><iframe src="https://maps.google.com/maps?q=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8D%83%E4%BB%A3%E7%94%B0%E5%8C%BA%E9%BA%B9%E7%94%BA1-4-4%20ZENITAKA%20ANNEX&amp;z=17&amp;hl=ja&amp;output=embed" title="株式会社エクスネットの地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div><p class="map-note">東京メトロ半蔵門線 半蔵門駅から徒歩3分　<a class="ex-ul" href="https://www.google.com/maps/search/?api=1&amp;query=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8D%83%E4%BB%A3%E7%94%B0%E5%8C%BA%E9%BA%B9%E7%94%BA1-4-4%20ZENITAKA%20ANNEX" target="_blank" rel="noopener">Googleマップで開く</a></p>
</div></section>

<section class="sec bg-alt" id="news"><div class="wrap">
{rule('お知らせ', True)}
<ul class="ex-news"><li><time datetime="2026-10-17">2026.10.17</time><span>コーポレートサイトをリニューアルしました</span></li></ul>
</div></section>

<section class="sec"><div class="wrap">
{rule('代表紹介', True)}
<div class="bio">{photo(False)}
<div><div class="bio__title">代表取締役／商談の伴走者</div><p class="bio__name">猪飼 智弘</p><div class="rep">{REP_BIO}</div>
<div class="mt-24">{more('代表メッセージを読む', 'message.html')}</div></div></div>
<div class="rows">
<a class="ex-row" href="message.html"><span>代表メッセージ</span>{circle()}</a><a class="ex-row" href="mission.html"><span>PMVV</span>{circle()}</a>
<a class="ex-row" href="#news"><span>お知らせ</span>{circle()}</a><a class="ex-row" href="privacy.html"><span>プライバシーポリシー</span>{circle()}</a>
</div></div></section>
'''
company = company.replace('<div class="rep">' + REP_BIO + '</div>', REP_BIO.replace('<ul>', '<ul class="list-dash">'))
doc('company.html', '会社情報', company, 'company')

# ====================================================================
# PMVV
# ====================================================================
mission = f'''
{phead([('ホーム', 'index.html'), ('会社情報', 'company.html'), ('PMVV', None)], 'COMPANY', 'PMVV', 'エクスネットが何のために、何を目指して仕事をしているかをお伝えします。', False)}
<section class="sec" style="padding-top:0"><div class="wrap wrap--narrow reading">
<h2 class="part"><small>PURPOSE</small>存在意義</h2><h3>「届ける力」で、社会を1ミリ前へ</h3>
<p>社会を良くする価値は、必要な人に届いてこそ意味を持ちます。</p>
<h2 class="part"><small>MISSION</small>使命</h2><h3>中小企業の可能性を引き出し、リスクを抑えながら成果を生み出す仕組みを共につくる</h3>
<p>私たちは中小企業の可能性を引き出し、リスクを抑えながら成果を生み出す仕組みを共につくります。</p>
<h2 class="part"><small>VISION</small>目指す姿</h2><h3>成果と想いを届けることにこだわり、選ばれ続けるブランドを目指す</h3>
<p>私たちは、成果と想いを届けることにこだわり、選ばれ続けるブランドを目指します。</p>
<h2 class="part"><small>VALUE</small>大切にしていること</h2>
<ol><li>好奇心を原動力に成長する</li><li>物事を多角的に捉え、プラス面に着目し行動する</li><li>遠回りを恐れず、着実に前進する</li><li>相手の立場に立ち、価値をわかりやすく伝えることを大切にする</li></ol>
<div class="end-links">{more('代表メッセージを読む', 'message.html')}{more('考え方を見る', 'approach.html')}</div>
</div></section>
'''
doc('mission.html', 'PMVV', mission, 'company')

# ====================================================================
# 代表メッセージ
# ====================================================================
msg = [
 ('元手も、特別なスキルもないところから始めました', [
  '20代の頃は、ウェブとはまったく関係のない飲食業界にいました。昼夜が逆転した生活で、1日12、13時間働く。これはいつか必ず限界が来ると思い、31歳で会社を立ち上げました。2011年6月、名古屋でのことです。',
  '元手はほとんどありませんでした。特別なスキルもなく、在庫を持つことも、商品を開発することもできない。だから、自分の手と足を動かして価値を届ける、形のない仕事を選ぶしかありませんでした。最初の仕事は、前の業界でお世話になった社長さんからいただいたホームページの制作です。最初は、本当に一人で全部やっていました。',
  'その後、自分でも講座をつくって販売してきました。広告をかけなくても講座が売れ、それだけで会社が回っていた時期もあります。物販の講座をパートナーと運営したこともあります。売る側の苦労も、売れなくなる怖さも、自分の事業で味わってきました。']),
 ('2度の苦い経験から、商談から入ると決めました', [
  '広告もLINEも、他社の規約ひとつで止まります。規約をしっかり守っていても、完全には防げません。',
  '弊社も過去に、自社の広告アカウントを2度止められました。他社の一存で、集客の入り口をいきなり切られる。そのとき売上が一気に止まり、自分では何ともできないもどかしさを味わいました。他社のプラットフォームだけで集客する怖さを、身をもって知りました。',
  '大事な事業を他社の一存で止めないために必要なのは、すでにある商談と、自社のリストを活かすことです。だから弊社は、広告より先に、商談と導線の見直しから入ります。そこで得た判断の基準を、御社の資産として残します。いまおすすめしていることは、すべてこの経験から来ています。']),
 ('丸投げをお受けしない理由', [
  '以前は、制作から運用まで丸ごとお引き受けしていたこともあります。けれど、作業が増えるばかりで、お客様の事業がなかなか前に進みませんでした。',
  '売るのは、お客様の商品です。お客様と直接お話しするのも、社長さんご自身です。丸投げしたくなるお気持ちは、私もよく分かります。それでも、全部を外に任せてしまうと、契約が終わったときにいちばん困るのはお客様です。',
  'だから弊社は、役割を分けて一緒に進めます。そのほうが、結局いちばん早いということを、失敗から学びました。広告の管理画面は頻繁に変わります。操作を覚えていただくより、何を見て、どう判断するかという基準を、御社の中に残していただきたいと考えています。弊社との契約が終わっても、ほかの会社に頼むことになっても、ご自身で決められるように。']),
 ('増えた売上からだけ、いただく理由', [
  '広告費の何割かを手数料としていただく形は、とっていません。その形にすると、運用する側は広告費を上げてもらうことが目的になってしまうからです。広告費を無駄に上げても、弊社には1円も返ってきません。',
  'お客様だけがリスクを取る形は、フェアではないと思っています。弊社がいただく成果報酬は、弊社が担当した経路から生まれた売上に対してだけです。お客様の売上が伸びなければ、弊社の売上も伸びません。正直に言えば、弊社も必死です。',
  '一方だけが得をする関係は、長く続きません。私自身、外の会社に仕事を頼んでうまくいかなかった経験が何度もあります。だから6ヶ月で一度区切り、続けるかどうかはお客様に決めていただくようにしています。']),
 ('毎週お会いできる数だけ、お受けしています', [
  '一度、手を広げてみようとしたことがありました。私の時間がまったく足りなくなり、すべてのお客様への支援が中途半端になってしまいました。',
  'それ以来、私が毎週お会いできる数だけをお受けしています。担当者を付けたら新人だった、ということは弊社では起こりません。私も必ず入ります。']),
 ('最後に責任を取るのは、人です', [
  '調べもの、分析、下書きの多くは、いまは機械に任せられます。けれど、お客様が欲しいのは道具ではなく、売上がどう変わるかです。最後に判断して責任を取るのは、人の仕事です。']),
 ('魔法は使えません。地味な仕事を、同じ方向を向いて', [
  '15年この仕事を続けてきても、やってみなければ分からないことはあります。だから「必ずこうなります」とはお約束しません。お約束できないことは売らない、と決めています。',
  '弊社の仕事は、数字を見て、詰まっている場所を一つ見つけ、直して、また数字を見る。その繰り返しです。正直に言って、地味な仕事です。けれど、すでにある商談で決まる件数が少し変わるだけで、売上は大きく変わります。',
  '同じ数字を見て、同じ方向を向いて、一緒に進めていければと思っています。'])]
message = f'''
{phead([('ホーム', 'index.html'), ('会社情報', 'company.html'), ('代表メッセージ', None)], 'COMPANY', '代表メッセージ', '広告より先に商談を見る。私がそう決めたのは、自分の事業で失敗したからです。', False)}
<section class="sec" style="padding-top:0"><div class="wrap wrap--narrow reading">
{photo()}
{''.join(f'<h3>{h}</h3>' + ''.join(f'<p>{p}</p>' for p in ps) for h, ps in msg)}
<div class="sign">株式会社エクスネット<br>代表取締役／商談の伴走者<b>猪飼 智弘</b></div>
<div class="end-links">{more('考え方を見る', 'approach.html')}{more('料金と契約を見る', 'price.html')}{more('PMVV', 'mission.html')}</div>
</div></section>
'''
doc('message.html', '代表メッセージ', message, 'company')

# ====================================================================
# 事例一覧・事例詳細
# ====================================================================
case = f'''
{hero([('ホーム', 'index.html'), ('事例', None)], '事例', 'お客様の支援と、弊社自身の取り組みの記録です。<br class="pc">数字は実数を、期間とあわせて載せています。', False)}
<section class="sec"><div class="wrap">
{dlbar()}
<div class="cards mt-64">
<a class="ex-ccard" href="case-edu.html"><div class="ex-ccard__img">{fig_change('31.3', '63.2', '%', '予約した面談に、来てくださった割合')}</div>
<div class="ex-ccard__cat">お客様の事例</div><h2 class="ex-ccard__title">高単価の教育サービスで、面談に来てくださる割合が31.3%から63.2%に</h2>
<div class="ex-ccard__aside">期間：6ヶ月<br>売上：1,206万円（ご成約17件）</div></a>
<a class="ex-ccard" href="case-exnet-btob.html"><div class="ex-ccard__img">{fig_funnel(FUN_BTOB, '面談の予約125件からご成約13件まで')}</div>
<div class="ex-ccard__cat">弊社自身の取り組み</div><h2 class="ex-ccard__title">弊社自身の高単価サービスで、面談95件からご成約13件、売上1,602万円</h2>
<div class="ex-ccard__aside">期間：2025年度（1商材）<br>ご成約1件あたり平均：約123万円<br>広告費：約188万円</div></a>
<a class="ex-ccard" href="case-exnet-form-dm.html"><div class="ex-ccard__img">{fig_funnel()}</div>
<div class="ex-ccard__cat">弊社自身の取り組み</div><h2 class="ex-ccard__title">843通の問い合わせフォーム営業から、面談11件・ご成約2件</h2>
<div class="ex-ccard__aside">商品の単価：約50万円<br>導線：個別メッセージ → 資料請求 → 面談 → ご成約</div></a>
</div>
<p class="note mt-64">お客様の事例は、社名を伏せ、業種だけを載せることにご了解をいただいています。数字は実数で、将来の成果を約束するものではありません。</p>
</div></section>
'''
doc('case.html', '事例', case, 'case')

case1 = f'''
<div class="ex-article"><div class="ex-article__box" style="max-width:var(--container)"><div style="max-width:var(--container-article);margin:0 auto">
{crumb([('ホーム', 'index.html'), ('事例', 'case.html'), ('843通の問い合わせフォーム営業から', None)])}
<div class="ex-ccard__cat">弊社自身の取り組み</div>
<h1>843通の問い合わせフォーム営業から、面談11件・ご成約2件</h1>
<div class="case-co">弊社自身（マーケティングの伴走支援）</div>
<div class="h-ov">プロジェクト概要</div>
{ov_table([('商品の単価', '約50万円'), ('導線', '個別メッセージ → 資料請求 → 面談 → ご成約'), ('送付数', '843通'), ('資料請求', '27件（3.2%）'), ('面談', '11件（1.3%）'), ('ご成約', '2件'), ('売上', '約100万円')])}
<div class="seebox"><h3>この数字の見方について</h3><p>弊社自身の営業の数字で、お客様の事例ではありません。送付先は、弊社がお役に立てそうな会社に絞っています。面談のなかで、弊社の支援が合わないと判断した会社にはお断りしました。同じ数字がほかの業種や商品で出るとは限りません。</p></div>
<h2>なぜ、自社で試したのか</h2>
<p>弊社は、お客様に「広告だけに頼らない集客の入り口」をおすすめしています。おすすめする以上、まず自社で試して、数字を確かめることにしました。</p>
<h2>何をしたか</h2>
<p>一斉に同じ文面を送るのではなく、相手の会社を調べ、その会社に向けた文面を1通ずつ用意しました。調べものと下書きには自社の仕組みを使い、送る前には必ず人が目を通しています。</p>
<h2>どうなったか</h2>
<p>843通を送り、27件の資料請求、11件の面談、2件のご成約につながりました。1,000通に届く前にご成約が生まれたことで、この入り口が弊社の事業でも使えることが分かりました。</p>
<h2>お客様の支援にどう生かしているか</h2>
<p>このやり方は、お客様のハウスリストへの働きかけにも使っています。これまでに失注したお客様にも、その方の状況に合わせた言葉で、もう一度ご連絡します。</p>
<div class="end-links">{more('考え方を見る', 'approach.html#systems')}{more('サービス', 'service.html')}{more('料金と契約', 'price.html')}</div>
</div></div></div>
'''
doc('case-exnet-form-dm.html', '843通の問い合わせフォーム営業から', case1, 'case')

def case_page(fname, crumb_t, cat, h1, pills, thead, tbody, seebox, secs, links):
    b = f'''
<div class="ex-article"><div class="ex-article__box" style="max-width:var(--container)"><div style="max-width:var(--container-article);margin:0 auto">
{crumb([('ホーム', 'index.html'), ('事例', 'case.html'), (crumb_t, None)])}
<div class="ex-ccard__cat">{cat}</div>
<h1>{h1}</h1>
<div class="case-co">{pills[0]}</div>
<div class="h-ov">プロジェクト概要</div>
{ov_table(pills[1:] + list(zip(thead, tbody)))}
<div class="seebox"><h3>この数字の見方について</h3><p>{seebox}</p></div>
{''.join(f'<h2>{h}</h2>' + ''.join(p if p.startswith('<') and not p.startswith(('<b>', '<strong>')) else f'<p>{p}</p>' for p in ps) for h, ps in secs)}
<div class="end-links">{''.join(more(l, h) for l, h in links)}</div>
</div></div></div>
'''
    doc(fname, crumb_t, b.replace('<div class="ex-numh__sub"></div>', ''), 'case')

case_page('case-edu.html', '高単価の教育サービス', 'お客様の事例',
  '高単価の教育サービスで、予約した面談に来てくださる割合が31.3%から63.2%に',
  ['高単価の教育サービス（個人のお客様向け）', ('期間', '6ヶ月'), ('弊社の役割', 'Facebook広告の運用と、支援全体')],
  ['期間', '売上', '広告費', 'LINE登録', 'ご成約'],
  ['6ヶ月', '1,206万円', '約412万円', '954件', '17件（面談で）'],
  'お客様の事例です。社名を伏せ、業種だけを載せることにご了解をいただいています。「広告費に対する売上」は、売上を広告費で割った値（ROAS）です。同じ数字がほかの業種や商品で出るとは限りません。',
  [('はじめの状態', ['ご一緒し始めたとき、予約した面談に実際に来てくださる方は、3人に1人ほど（31.3%）でした。月の売上は、その月の広告費の90%で、広告費を下回っていました。']),
   ('何をしたか', ['6ヶ月間、Facebook広告の運用と、その先のご支援をご一緒しました。']),
   ('どうなったか', ['予約した面談に来てくださる割合は、31.3%から63.2%になり、2人に1人を超えました。月の広告費に対する売上は、90%から466%まで上がりました。',
     '<div class="tbl-wrap"><table><thead><tr><th>見た数字</th><th>開始時</th><th>期間中</th></tr></thead><tbody>'
     '<tr><td>予約した面談に、来てくださった割合</td><td>31.3%</td><td>63.2%</td></tr>'
     '<tr><td>月の広告費に対する売上（ROAS）</td><td>90%</td><td>466%</td></tr></tbody></table></div>',
     '数字が整ってきた後半の3ヶ月は、広告費に対する売上が328%、月の売上は平均259万円でした。6ヶ月の合計は、LINE登録954件、ご成約17件、売上1,206万円です。']),
   ('この事例から言えること', ['広告で集めた方が面談に来てくださらなければ、その分の広告費は何も生みません。来てくださる割合が2倍になれば、同じ広告費のままで、お話しできる方が2倍になります。広告を増やす前に、面談までの流れを見直す理由は、ここにあります。'])],
  [('考え方を見る', 'approach.html'), ('サービス', 'service.html'), ('料金と契約', 'price.html')])

case_page('case-exnet-btob.html', '弊社自身の高単価サービス', '弊社自身の取り組み',
  '弊社自身の高単価サービスで、面談95件からご成約13件、売上1,602万円',
  ['弊社自身（法人向けの高単価サービス）', ('期間', '2025年度（1商材）')],
  ['期間', '面談の予約', '面談', 'ご成約', '売上', 'ご成約1件あたり', '広告費'],
  ['2025年度', '125件', '95件（76%）', '13件', '1,602万円', '平均 約123万円', '約188万円'],
  '弊社自身の数字で、お客様の事例ではありません。2025年度に販売した1つの商品の数字です。同じ数字がほかの業種や商品で出るとは限りません。',
  [('なぜ、自社の数字を載せるのか', ['お客様におすすめしていることは、まず自社の商品で確かめています。これは、そのうちの1つの商品の、1年分の数字です。']),
   ('どうなったか', ['面談のご予約は125件で、そのうち95件（76%）の方が実際に面談に来てくださいました。そこから13件のご成約につながり、売上は1,602万円でした。ご成約1件あたりの平均は約123万円です。広告費は約188万円で、売上は広告費の約8.5倍（ROAS 約854%）です。']),
   ('お客様の支援にどう生かしているか', ['面談の予約、実際の面談、ご成約の3つを、毎月同じ形で数えています。お客様の支援でも、この3つの数字を毎週の報告に載せ、どこで止まっているかを一緒に見ます。'])],
  [('考え方を見る', 'approach.html'), ('サービス', 'service.html'), ('料金と契約', 'price.html')])


# ====================================================================
# 資料請求・無料相談・送信完了
# ====================================================================
SRC = '<option value="">選んでください</option><option>DM</option><option>ご紹介</option><option>検索</option><option>SNS</option><option>その他</option>'
PRICE_OPT = '<option value="">選んでください</option><option>30万円未満</option><option>30万〜100万円</option><option>100万円以上</option>'
def checks(name, items): return '<span class="checks">' + ''.join(f'<label><input type="checkbox" name="{name}" value="{i}"> {i}</label>' for i in items) + '</span>'
CH = ['紹介', '広告', 'SNS', 'LINE・メルマガ', 'セミナー', 'その他']
def steps_bar(): return '<div class="ex-steps" aria-hidden="true"><i class="is-current">1</i><span>ご連絡先</span><i>2</i><span>会社のこと</span><i>3</i><span>ご相談の内容</span></div>'

FORM_JS = '''<script>
(function(){var f=document.querySelector('form[data-steps]');if(!f)return;var ps=f.querySelectorAll('[data-step]'),dots=f.querySelectorAll('.ex-steps i'),n=0;
function show(i,first){n=i;ps.forEach(function(p,k){p.hidden=k!==i});dots.forEach(function(d,k){d.classList.toggle('is-current',k===i)});if(first)return;var r=f.getBoundingClientRect();if(r.top<0)f.scrollIntoView({block:'start'});var h=f.querySelector('[data-step]:not([hidden]) input,[data-step]:not([hidden]) select');if(h)h.focus({preventScroll:true});}
function ok(p){var good=true;p.querySelectorAll('.field-err').forEach(function(e){e.remove()});
p.querySelectorAll('[required]').forEach(function(el){var bad=el.type==='checkbox'?!el.checked:!el.value.trim();if(bad){good=false;var s=document.createElement('span');s.className='field-err';s.textContent=el.type==='checkbox'?'同意いただくと送信できます':el.tagName==='SELECT'?'選んでください':'入力してください';el.closest('label').appendChild(s);}});
var g=p.querySelector('[data-need-one]');if(g&&!g.querySelector('input:checked')){good=false;var s=document.createElement('span');s.className='field-err';s.textContent='1つ以上選んでください';g.appendChild(s);}return good;}
f.querySelectorAll('[data-next]').forEach(function(b){b.addEventListener('click',function(){if(ok(ps[n]))show(n+1)})});
f.querySelectorAll('[data-back]').forEach(function(b){b.addEventListener('click',function(){show(n-1)})});
var fit=f.querySelector('.fit');if(fit){var pr=f.querySelector('#c-price'),sl=f.querySelector('#c-sell');function chk(){fit.hidden=!(pr.value==='30万円未満'||(sl&&sl.value==='no'))}pr.addEventListener('change',chk);if(sl)sl.addEventListener('change',chk);}
f.addEventListener('submit',function(e){e.preventDefault();if(!ok(ps[n]))return;if(f.getAttribute('action'))f.submit();else location.href=f.getAttribute('data-thanks');});show(0,true);})();
</script>'''

SLOT_JS = '''<script>
(function(){var ss=document.querySelectorAll('select[data-slot]');if(!ss.length)return;var W='日月火水木金土',T=['10:00','11:00','13:00','14:00','15:00','16:00','17:00'],d=new Date(),k=0,o='';d.setHours(0,0,0,0);
while(k<12){d.setDate(d.getDate()+1);var w=d.getDay();if(w===0||w===6)continue;k++;if(k<2)continue;var md=(d.getMonth()+1)+'月'+d.getDate()+'日（'+W[w]+'）';o+='<optgroup label="'+md+'">'+T.map(function(t){return '<option>'+md+' '+t+'〜</option>'}).join('')+'</optgroup>';}
ss.forEach(function(s){s.insertAdjacentHTML('beforeend',o)});})();
</script>'''

download = f'''<div class="lp">
<div class="lp__body"><h1>サービス資料の<br class="pc">ご請求</h1>
<p>サイトでご紹介しているサービス内容を、図解入りの1冊にまとめました。社内で回覧しやすいPDFでお送りします。DMでご案内している資料と同じものです。</p>
<p>ご入力いただいたメールアドレスに、すぐにお送りします。</p>
<h2>資料に入っていること</h2>
<ul class="list-dash"><li>商談から入る理由と、4つの打ち手の順番</li><li>伴走型と伴走＋実務型の違い</li><li>月額、成果報酬、契約期間の条件</li><li>最初の2週間でお渡しするもの</li></ul>
<h2>別の窓口</h2><p style="margin-top:var(--space-8)">いまのご商談を直接見てほしい方は</p>{more('無料相談へ', 'contact.html')}
</div>
<form class="ex-form" action="https://ut.exnet.biz/r/YpY0rGMHY4MT/store" method="post" data-steps data-thanks="thanks-download.html" novalidate>
<p class="ex-form__note">4項目だけ、30秒ほどで終わります。</p>
<div data-step>
<label class="ex-field" for="d-name">お名前 <em>*</em><input id="d-name" name="name" autocomplete="name" required></label>
<label class="ex-field" for="d-mail">メールアドレス <em>*</em><input id="d-mail" type="email" name="mail" autocomplete="email" required></label>
<label class="ex-field" for="d-co">会社名 <em>*</em><input id="d-co" name="free93" autocomplete="organization" required></label>
<label class="agree" for="d-agree"><input id="d-agree" type="checkbox" required> <span><a href="privacy.html" target="_blank" rel="noopener">個人情報の取り扱い</a>に同意する <em style="color:var(--required);font-style:normal">*</em></span></label>
<button type="submit" class="ex-submit">資料を受け取る</button></div>
</form></div>'''
doc('download.html', '資料請求', download, lp=True, extra_js=FORM_JS)

contact = f'''<div class="lp">
<div class="lp__body"><h1>無料相談<br><small style="font-size:16px;font-weight:500">オンライン45分</small></h1>
<p>45分で、いまのご商談と導線のどこから手を付けるとよいかが分かります。</p>
<p>ご契約を前提にしたご相談ではありません。お話を伺ったうえで、弊社ではお力になれないと判断した場合は、正直にそうお伝えします。</p>
<p>お名前などをご入力のうえ、日時を選んでお申し込みください。その場で日程が決まります。</p>
<h2>相談で伺うこと</h2>
<ul class="list-dash"><li>いまの商品・サービスと単価</li><li>月の面談数と、決まる件数のおおよそ</li><li>いまの集客の経路と、LINEやメールのリストの状況</li></ul>
<p class="note">事前にご用意いただけると助かるもの：直近のご商談の録画、トークスクリプト、提案資料のいずれか1つ。なくてもご相談いただけます。</p>
<h2>別の窓口</h2><p style="margin-top:var(--space-8)">まずは資料で確かめたい方は</p>{more('資料請求へ', 'download.html')}
<p class="note">その他のお問い合わせ（取材・協業など）：<a class="ex-ul" href="mailto:info@exnet.biz">info@exnet.biz</a></p>
</div>
</div>'''
REF_JS = '<script>(function(){var s=document.getElementById("c-src"),w=document.getElementById("c-ref-wrap");if(s&&w)s.addEventListener("change",function(){w.hidden=s.value!=="ご紹介"});})();</script>'

# 予約は2段階（1画面目の入力内容を、UTAGEのファネルページの予約フォームに受け渡す）。仕組みは design/utage/booking/README.md
BOOK_SRC = 'https://ut.exnet.biz/p/sA61r06GNKyM'
opts = lambda xs: ''.join(f'<option>{x}</option>' for x in xs)
contact2 = contact[:-len("</div>")] + f'''<div class="book" data-book>
<div class="ex-form"><p class="ex-form__note">お客様の情報をご入力いただき、次の画面で日時を選ぶと、その場で予約が確定します。オンライン会議のURLは、確定のメールでお送りします。</p>
<p class="fit fit--static">弊社の支援が力を発揮するのは、販売単価30万円以上の商品・サービスをメインで扱われている事業者様です。当てはまるか迷われた方は、先に資料請求でお確かめいただくこともできます。<br><a href="download.html">資料請求はこちら</a></p>
<div data-book-step>
<div class="ex-field-row"><label class="ex-field" for="b-sei">姓 <em>*</em><input id="b-sei" name="sei" autocomplete="family-name" required></label><label class="ex-field" for="b-mei">名 <em>*</em><input id="b-mei" name="mei" autocomplete="given-name" required></label></div>
<label class="ex-field" for="b-mail">メールアドレス <em>*</em><input id="b-mail" type="email" name="mail" autocomplete="email" required></label>
<label class="ex-field" for="b-tel">携帯番号 <em>*</em><input id="b-tel" type="tel" name="phone" autocomplete="tel" inputmode="tel" required></label>
<label class="ex-field" for="b-co">会社名 <em>*</em><input id="b-co" name="event_item01" autocomplete="organization" required></label>
<label class="ex-field" for="b-price">商品・サービスの単価 <em>*</em><select id="b-price" name="event_item02" required><option value="">選んでください</option>{opts(['30万円未満', '30万〜100万円', '100万円以上'])}</select></label>
<label class="ex-field" for="b-topic">いちばんご相談したいこと <em>*</em><select id="b-topic" name="event_item03" required><option value="">選んでください</option>{opts(['商談で決まる件数', 'リストの活用', '広告', '全体を見てほしい'])}</select></label>
<label class="agree" for="b-agree"><input id="b-agree" type="checkbox" required> <span><a href="privacy.html" target="_blank" rel="noopener">個人情報の取り扱い</a>に同意する <em style="color:var(--required);font-style:normal">*</em></span></label>
<button type="button" class="ex-submit" data-book-next>日時の選択へ進む</button></div>
<div class="book__who" data-book-who hidden><span data-book-name></span><button type="button" class="back" data-book-back>入力内容を修正する</button></div>
<p class="book__retry" data-book-retry hidden>お手数ですが、下の欄にお名前などをもう一度ご入力ください。</p></div>
<iframe class="book__cal" data-book-frame title="無料相談の日時の選択" hidden></iframe>
<p class="book__alt">日時の選択が表示されない場合は、<a href="{BOOK_SRC}" target="_blank" rel="noopener">予約ページを別の画面で開く</a>からお申し込みください。</p>
</div></div>'''
BOOK2_JS = open(os.path.join(os.path.dirname(__file__), 'book2.js')).read().replace('%SRC%', BOOK_SRC)
doc('contact.html', '無料相談', contact2, lp=True, extra_js=BOOK2_JS)

def thanks(fname, h1, body, links, skip):
    b = f'''{phead([('ホーム', 'index.html'), (h1, None)], 'THANK YOU', h1, body, False)}
<section class="sec" style="padding-top:0"><div class="wrap wrap--narrow"><div class="end-links" style="margin-top:0">{''.join(more(l, h) for l, h in links)}</div></div></section>'''
    doc(fname, h1, b, fcta_skip=skip)
thanks('thanks-download.html', '資料をお送りしました', 'ご入力いただいたメールアドレスに、資料をお送りしました。<br class="pc">届いていない場合は、迷惑メールのフォルダもご確認ください。',
       [('考え方を読む', 'approach.html'), ('無料相談を申し込む', 'contact.html')], 'download')
thanks('thanks-contact.html', 'お申し込みありがとうございます', 'ご予約の内容と、オンライン会議のURLをメールでお送りしました。ご商談の録画や資料があれば、当日までにお送りいただけると、より具体的なお話ができます。',
       [('料金と契約を見る', 'price.html'), ('代表メッセージを読む', 'message.html')], 'contact')

# ====================================================================
# プライバシーポリシー（たたき台）
# ====================================================================
POLICY = [
 ('1. 基本方針', ['株式会社エクスネット（以下「弊社」）は、お客様からお預かりする個人情報の大切さを認識し、個人情報の保護に関する法律その他の法令を守り、以下の方針にもとづいて適切に取り扱います。'], None),
 ('2. 取得する個人情報', ['弊社は、次の場面で、必要な範囲の個人情報を取得します。'],
  ['資料請求・無料相談のお申し込み：お名前、メールアドレス、電話番号、会社名、商品・サービスの単価、集客の経路、ご相談の内容など',
   'ご契約とご支援：ご担当者様の連絡先、請求に必要な情報、ご提供いただく商談の録画・トークスクリプト・資料、面談数・成約数などの数字',
   'お問い合わせ：お名前、ご連絡先、お問い合わせの内容']),
 ('3. 利用目的', ['取得した個人情報は、次の目的の範囲で利用します。'],
  ['資料の送付、無料相談の日程調整と実施','ご契約にもとづく支援の提供、毎週の報告、月末のレビュー','料金のご請求と決済','お問い合わせへの回答','サービスやお知らせのご案内（ご不要の場合は、いつでも停止できます）','サービスの改善のための分析（個人を特定しない形で行います）']),
 ('4. 第三者への提供', ['弊社は、次の場合を除き、ご本人の同意なく個人情報を第三者に提供しません。'],
  ['法令にもとづく場合','人の生命、身体または財産の保護のために必要で、ご本人の同意を得ることが難しい場合','国の機関などが法令の定める事務を行うことに協力する必要がある場合']),
 ('5. 業務の委託', ['弊社は、利用目的の達成に必要な範囲で、個人情報の取り扱いを外部に委託することがあります（例：フォームとメール配信のシステム、決済、支援の実務を担う業務委託先）。委託先は、個人情報を適切に扱えることを確かめたうえで選び、必要な監督を行います。'], None),
 ('6. 安全管理', ['弊社は、個人情報の漏えい、滅失または毀損を防ぐため、アクセスできる人の限定、パスワードの管理、委託先の監督など、必要で適切な措置をとります。お預かりした商談の録画や資料は、支援の目的以外には使いません。'], None),
 ('7. Cookie とアクセス解析', ['当サイトでは、利用状況を把握するため、Cookie を使ったアクセス解析を行う場合があります。取得する情報に、個人を特定するものは含まれません。Cookie は、ブラウザの設定で無効にできます。'], None),
 ('8. 開示・訂正・利用停止などのご請求', ['ご本人から、ご自身の個人情報の利用目的の通知、開示、訂正、追加、削除、利用停止、第三者への提供の停止を求められた場合は、ご本人であることを確かめたうえで、法令にもとづき速やかに対応します。ご請求は、下記の窓口までご連絡ください。'], None),
 ('9. このポリシーの変更', ['弊社は、法令の改正や事業の変化にあわせて、このポリシーを変更することがあります。変更後の内容は、このページに掲載した時点から効力を持ちます。'], None),
]
pol_body = ''.join(f'<h3>{h}</h3>' + ''.join(f'<p>{t}</p>' for t in ps) + (f'<ol class="items">' + ''.join(f'<li>{i}</li>' for i in li) + '</ol>' if li else '') for h, ps, li in POLICY)
privacy = f"""
{phead([('ホーム', 'index.html'), ('会社情報', 'company.html'), ('プライバシーポリシー', None)], 'PRIVACY POLICY', 'プライバシーポリシー', 'お預かりする個人情報の取り扱いについて、弊社の方針をお伝えします。', False)}
<section class="sec" style="padding-top:0"><div class="wrap wrap--narrow reading policy">
{pol_body}
<h3>10. お問い合わせの窓口</h3>
<dl class="ex-dl"><dt>事業者</dt><dd>株式会社エクスネット</dd><dt>所在地</dt><dd>〒102-0083 東京都千代田区麹町1-4-4 ZENITAKA ANNEX 2F</dd><dt>代表者</dt><dd>代表取締役　猪飼 智弘</dd><dt>電話番号</dt><dd>03-6262-1694</dd><dt>メール</dt><dd><a class="ex-ul" href="mailto:info@exnet.biz">info@exnet.biz</a></dd></dl>
</div></section>
"""
doc('privacy.html', 'プライバシーポリシー', privacy, 'company')

# ---------- 404（旧サイトのURLや打ち間違いで来た方を、トップと主なページへ戻す） ----------
notfound = f"""
{phead([('ホーム', 'index.html'), ('ページが見つかりません', None)], 'NOT FOUND', 'ページが見つかりません', 'お探しのページは、移動したか削除された可能性があります。サイトを新しくしたため、以前のURLが変わっています。', False)}
<section class="sec" style="padding-top:0"><div class="wrap wrap--narrow reading">
<ol class="list-dash" style="list-style:none"><li><a class="ex-ul" href="index.html">トップページ</a></li><li><a class="ex-ul" href="service.html">サービス</a></li><li><a class="ex-ul" href="price.html">料金と契約</a></li><li><a class="ex-ul" href="company.html">会社情報</a></li><li><a class="ex-ul" href="column.html">コラム</a></li><li><a class="ex-ul" href="contact.html">無料相談</a></li></ol>
</div></section>
"""
doc('404.html', 'ページが見つかりません', notfound)
# 404 は深い階層のURLでも表示されるので、相対リンクがサイトのルートを指すようにする
_p = os.path.join(OUT, '404.html'); _h = open(_p, encoding='utf-8').read()
open(_p, 'w', encoding='utf-8').write(_h.replace('<head>', '<head><base href="/">', 1))

# ====================================================================
# コラム（悩みの言葉で検索する方の入口）
# ====================================================================
AUTHOR_BOX = (f'<div class="col-author"><img src="ikai.webp" alt="猪飼 智弘" width="88" height="88" loading="lazy">'
              '<div><span class="col-author__label">この記事を書いた人</span><b>猪飼 智弘</b><span class="col-author__role">株式会社エクスネット 代表取締役／商談の伴走者</span>'
              '<p>2011年に名古屋で創業。自社でも講座の販売や広告の運用を続けながら、面談で販売する高単価の商品・サービスの売上を、商談と導線から伸ばす伴走支援をしています。</p>'
              f'{more("代表メッセージ", "message.html")}</div></div>')

def column(fname, title, date, lead, answer, secs, links, desc, faqs=()):
    """記事1本。answer は冒頭で問いに一文で答える箇所（AIの引用を受けやすい）"""
    COLUMNS[fname] = {'title': title, 'date': date, 'lead': lead}
    DESC[fname] = desc
    body = f"""
<div class="ex-article"><div class="ex-article__box" style="max-width:var(--container)"><div style="max-width:var(--container-article);margin:0 auto">
{crumb([('ホーム', 'index.html'), ('コラム', 'column.html'), (title, None)])}
<div class="ex-ccard__cat">コラム<span class="col-date">{date.replace('-', '.')}</span></div>
<h1>{title}</h1>
<div class="seebox col-answer"><h3>先に結論</h3><p>{answer}</p></div>
{''.join(f'<h2>{h}</h2>' + ''.join(p if p.startswith('<') and not p.startswith(('<b>', '<strong>')) else f'<p>{p}</p>' for p in ps) for h, ps in secs)}
{('<h2>よくある質問</h2>' + faq(faqs)) if faqs else ''}
{AUTHOR_BOX}
<div class="end-links">{''.join(more(l, h) for l, h in links)}</div>
</div></div></div>
"""
    doc(fname, title, body, 'column')

for _p in sorted(glob.glob(os.path.join(HERE, 'columns', '*.json'))):
    _c = json.load(open(_p, encoding='utf-8'))
    column(_c['fname'], _c['title'], _c.get('date', '2026-10-17'), _c['lead'], _c['answer'], _c['secs'], _c['links'], _c['desc'], _c.get('faqs', []))

col_list = ''.join(
    f'<a class="col-row" href="{f}"><span class="col-date">{c["date"].replace("-", ".")}</span><span class="col-row__t">{c["title"]}</span><span class="col-row__l">{c["lead"]}</span>{circle()}</a>'
    for f, c in sorted(COLUMNS.items(), key=lambda kv: kv[1]['date'], reverse=True))
DESC['column.html'] = '面談で販売する高単価の商品・サービスの売上を、商談と導線から伸ばすためのコラムです。成約率、面談に来てくださる割合、リストの活用など、日々の支援で分かったことを書いています。'
column_index = f"""
{hero([('ホーム', 'index.html'), ('コラム', None)], 'コラム', '面談で販売する高単価の商品・サービスの売上を、<br class="pc">商談と導線から伸ばすために、日々の支援で分かったことを書いています。', False)}
<section class="sec"><div class="wrap wrap--article"><div class="col-list">{col_list}</div></div></section>
"""
doc('column.html', 'コラム｜高単価の商品・サービスの成約率と商談の話', column_index, 'column')


print('built:', sorted(os.listdir(OUT)))


# ---------- サイトマップ・robots.txt・llms.txt ----------
today = datetime.date.today().isoformat()
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in PAGES) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
LLMS_NAMES = {'index.html': 'トップ', 'service.html': 'サービス', 'price.html': '料金と契約', 'approach.html': '考え方',
              'company.html': '会社情報', 'mission.html': 'PMVV', 'message.html': '代表メッセージ', 'case.html': '事例',
              'case-edu.html': '事例：高単価の教育サービス', 'case-exnet-btob.html': '事例：弊社自身の高単価サービス', 'case-exnet-form-dm.html': '事例：問い合わせフォーム営業',
              'column.html': 'コラム', 'column-before-ads.html': 'コラム：広告費を増やす前に、確かめたい3つの数字',
              'column-ad-fee.html': 'コラム：広告代理店の手数料と成果報酬の違い', 'column-lost-deals.html': 'コラム：決まらなかったお客様へのご連絡', 'column-platform-risk.html': 'コラム：広告やLINEが止まったときの備え', 'column-outsourcing.html': 'コラム：マーケティングの丸投げがうまくいかない理由',
              'column-no-show.html': 'コラム：予約した面談に来てもらえないとき', 'column-line-consult.html': 'コラム：LINEから個別相談の申し込みが来ないとき', 'column-cost-per-meeting.html': 'コラム：広告を面談1件あたりの広告費で見る',
              'download.html': '資料請求', 'contact.html': '無料相談', 'privacy.html': 'プライバシーポリシー'}
open(os.path.join(OUT, 'llms.txt'), 'w').write(
    f'# {SITE_NAME}\n\n> {DESC["index.html"]}\n\n'
    '- 所在地：東京都千代田区麹町1-4-4 ZENITAKA ANNEX 2F\n- 代表取締役：猪飼 智弘\n- 創業：2011年6月（名古屋）\n- お問い合わせ：info@exnet.biz\n\n## ページ\n\n' +
    ''.join(f'- [{LLMS_NAMES.get(u.replace(BASE, "") or "index.html") or ("コラム：" + COLUMNS[u.replace(BASE, "")]["title"].split("｜")[0] if u.replace(BASE, "") in COLUMNS else u)}]({u})：{DESC.get(u.replace(BASE, "") or "index.html", "")}\n' for u in PAGES))
