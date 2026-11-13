#!/usr/bin/env python3
"""Генератор сайта «Коммерческое предложение» (вертикальный лендинг в стиле Концентрата).
Запуск: python3 -I build_site.py   (из любой папки). Данные кейсов и шагов берутся из презентации."""
import os, html, struct

B = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(B)
IMG = OUT + '/assets/img/'
PRES = os.path.join(os.path.dirname(OUT), 'kp-presentation', '_source', 'build.py')
NB = ' '
TG = 'https://t.me/vitalijlugovoj'
CHANNEL = 'https://t.me/+5BSQKpWBD1Q3OGFi'
REVIEWS = 'https://t.me/otzvzapusk'


def esc(s):
    return html.escape(s, quote=False)


RING = {'p12_X42', 'p15_X50', 'p33_X87', 'p33_X88', 'p33_X89', 'p33_X90', 'p33_X91', 'p34_X92', 'p34_X93', 'p34_X94', 'p34_X95', 'p34_X96'}


def rn(name):
    """кружки-отзывы обрезаны по внутреннему краю кольца и лежат под именем *_r.jpg"""
    base = name[:-4] if name.endswith('.jpg') else name
    return base + '_r.jpg' if base in RING else name


def img_size(path):
    d = open(os.path.join(os.path.dirname(path), rn(os.path.basename(path))), 'rb').read()
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', d[16:24])
    i = 2
    while i < len(d):
        if d[i] != 0xFF:
            i += 1
            continue
        m = d[i + 1]
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack('>HH', d[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack('>H', d[i + 2:i + 4])[0]
    return 1, 1


def ratio(name):
    w, h = img_size(IMG + name)
    return w / h


def hd(lines, cls='', d=0.0):
    return '<h2 class="hd %s">%s</h2>' % (cls, ''.join(
        '<span class="ln"><i style="--i:%d;--d:%ss">%s</i></span>' % (i, d, l) for i, l in enumerate(lines)))


def a(kind, d=0.0):
    return 'data-a="%s" style="--d:%ss"' % (kind, d)


def link(href, label, cls='lk', d=None):
    at = ' ' + a('up', d) if d is not None else ''
    return '<a class="%s" href="%s" target="_blank" rel="noopener noreferrer"%s>%s</a>' % (cls, href, at, label)


def money(n):
    return '{:,}'.format(n).replace(',', NB)


def img(name, lazy=True, alt='', extra=''):
    w, h = img_size(IMG + name)
    return '<img src="assets/img/%s" width="%d" height="%d" alt="%s"%s%s>' % (rn(name), w, h, alt, ' loading="lazy" decoding="async"' if lazy else '', extra)


# --- данные из презентации (кейсы и шаги) ---
src = open(PRES, encoding='utf8').read()
ns = {'REVIEWS': REVIEWS, 'TG': TG}
exec(src[src.index('cases = ['):src.index('def case_slide')], ns)
exec(src[src.index('steps = ['):src.index('for n, t, txt, im, cap, note in steps')], ns)
cases = ns['cases']
steps = ns['steps']

for c in cases:
    if c['id'] == 'c7':
        c['gal'] = [dict(img=['p26_X77.jpg'], cap='Изучить проект подробнее', href='https://alabaster-argon-e03.notion.site/4-6cbb532d0c554d2996e51019e11bc851?pvs=4', hl='Изучить проект')]
    else:
        c['gal'] = c['proof']['cards']
cases.append(dict(id='c9', n=9, tag='Личный запуск', lines=['Свой личный', 'запуск за <em>2 недели</em>'], sum=1000000, sumlabel='Результат', reach=None,
                  href='https://teletype.in/@vitaliy.lugovoj/vuhYHM8R_1_', hlabel='Подробный разбор запуска', hsolid=True,
                  short='Свой личный запуск', sumtxt='1 000 000 ₽', sumnote='за 2 недели',
                  det='Свой личный запуск на 1 000 000 ₽ за 2 недели: реалити-шоу «Миллионный запуск». Все шаги и воронки — в подробном разборе по ссылке.', did=None,
                  gal=[dict(img=['p32_X86.jpg'], cap='Реалити-шоу «Миллионный запуск»', href='https://teletype.in/@vitaliy.lugovoj/vuhYHM8R_1_', hl='Подробный запуск')]))

# маленький золотой сейф со стопками таких же монет; в прорезь на крышке падает монетка (см. site.js)
def _stack(cx, base, n):
    return ''.join('<ellipse cx="%d" cy="%d" rx="11" ry="4" fill="url(#sgc)" stroke="#8f5d0e" stroke-width="1"/>' % (cx, base - 4 * k) for k in range(n))


_ticks = ''.join('<line x1="60" y1="51" x2="60" y2="54.5" stroke="#7a4f0a" stroke-width="1.6" transform="rotate(%d 60 66)"/>' % (45 * k) for k in range(8))
SAFE = '''<svg class="safe" viewBox="0 0 170 132" role="img" aria-label="Золотой сейф с монетами">
<defs>
<linearGradient id="sgb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe493"/><stop offset=".5" stop-color="#e5ad34"/><stop offset="1" stop-color="#9a6410"/></linearGradient>
<linearGradient id="sgd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6c850"/><stop offset="1" stop-color="#b9801c"/></linearGradient>
<radialGradient id="sgc" cx=".32" cy=".26" r=".95"><stop offset="0" stop-color="#fff6c2"/><stop offset=".35" stop-color="#f7cd4a"/><stop offset=".7" stop-color="#d49a1f"/><stop offset="1" stop-color="#8f5d0e"/></radialGradient>
</defs>
<ellipse cx="85" cy="125" rx="80" ry="4" fill="rgba(0,0,0,.35)"/>
<rect x="22" y="112" width="14" height="10" rx="2" fill="#8f5d0e"/><rect x="84" y="112" width="14" height="10" rx="2" fill="#8f5d0e"/>
<rect x="10" y="17" width="100" height="97" rx="9" fill="url(#sgb)" stroke="#7a4f0a" stroke-width="2"/>
<rect x="14" y="10" width="92" height="12" rx="5" fill="#f8d36a" stroke="#7a4f0a" stroke-width="2"/>
<rect x="38" y="13" width="44" height="5" rx="2.5" fill="#2a1a05"/>
<rect x="22" y="30" width="76" height="72" rx="6" fill="url(#sgd)" stroke="#7a4f0a" stroke-width="2"/>
<rect x="28" y="36" width="64" height="60" rx="4" fill="none" stroke="#fff0b0" stroke-opacity=".5"/>
<rect x="17" y="40" width="6" height="11" rx="2" fill="#7a4f0a"/><rect x="17" y="80" width="6" height="11" rx="2" fill="#7a4f0a"/>
<g class="dial"><circle cx="60" cy="66" r="18" fill="#ebb73f" stroke="#7a4f0a" stroke-width="2"/>''' + _ticks + '''<circle cx="60" cy="66" r="10" fill="#c78a1e" stroke="#7a4f0a" stroke-width="1.5"/>
<line x1="60" y1="66" x2="60" y2="57" stroke="#5a3905" stroke-width="2.4" stroke-linecap="round"/><line x1="60" y1="66" x2="67" y2="70" stroke="#5a3905" stroke-width="2.4" stroke-linecap="round"/><line x1="60" y1="66" x2="53" y2="70" stroke="#5a3905" stroke-width="2.4" stroke-linecap="round"/></g>
''' + _stack(131, 118, 5) + _stack(153, 118, 3) + '''
<ellipse cx="142" cy="120" rx="11" ry="3" fill="rgba(0,0,0,.25)"/>
<g transform="rotate(-18 150 94)"><ellipse cx="150" cy="94" rx="10" ry="10" fill="url(#sgc)" stroke="#8f5d0e" stroke-width="1.2"/><text x="150" y="98" text-anchor="middle" font-size="11" font-weight="900" fill="#8f5d0e" font-family="Arial Narrow,Arial,sans-serif">₽</text></g>
</svg>'''

secs = []  # html блоки
counter = [0]


def folio(title):
    counter[0] += 1
    n = '%02d' % counter[0]
    return n, '<div class="folio"><span><b>%s</b> · %s</span><span>Коммерческое предложение</span></div>' % (n, esc(title))


def section(sid, title, body, cls='', gx='50%', gy='60%', bignum=None):
    n, f = folio(title)
    big = '<div class="bignum" aria-hidden="true">%s</div>' % bignum if bignum else ''
    secs.append('<section class="sec %s" id="%s" data-num="%s" data-title="%s" style="--gx:%s;--gy:%s">%s%s%s</section>' % (
        cls, sid, n, esc(title), gx, gy, f, big, body))


# ---------------------------------------------------------------- ОБЛОЖКА
counter[0] += 1
secs.append(f'''<header class="cover" id="top" data-num="01" data-title="Обложка">
<div class="strip"><span>@lugovoy.vitaliy</span><span>Запуски онлайн-школ · Москва</span></div>
<div class="cstage">
<h1 class="mast"><span class="ln"><i>Коммерческое</i></span><span class="ln"><i>предложение</i></span></h1>
<p class="sub" {a('up', .35)}>по запускам от Виталия Лугового</p>
<img class="fig" src="assets/img/portrait.png" width="541" height="950" alt="Виталий Луговой" {a('z', .25)}>
<div class="left">
  <p class="motto" {a('up', .5)}>Помогаю экспертам делать миллионные запуски</p>
  <p {a('up', .62)}>Берусь за запуск под ключ: от анализа аудитории и&nbsp;распаковки до прогрева, вебинара и&nbsp;продаж.</p>
  <p {a('up', .72)}>За 5&nbsp;лет продал курсов на <b>150+ миллионов&nbsp;₽</b></p>
  <p class="free" {a('up', .82)}>@lugovoy.vitaliy · Москва</p>
</div>
<div class="right">
  <div class="line" {a('r', .7)}><small>Опыт</small><strong>150+ млн ₽</strong><span>продано курсов за 5 лет</span></div>
  <div class="line" {a('r', .85)}><small>Ученики</small><strong>40+</strong><span>обучил запускам</span></div>
  <div class="line" {a('r', 1.0)}><small>Максимум</small><strong>18 млн ₽</strong><span>за один запуск эксперта</span></div>
</div>
<a class="go" href="{TG}" target="_blank" rel="noopener noreferrer" {a('up', 1.1)}>Обсудить запуск</a>
</div>
</header>''')

# ---------------------------------------------------------------- ОБО МНЕ
section('about', 'Обо мне', f'''
<div class="wrap">
  <div>
    <div class="kicker"><b>@lugovoy.vitaliy</b></div>
    <div style="margin-top:20px">{hd(['Привет, я', 'Виталий'], 'xl')}</div>
    <p class="lead" {a('up', .3)}>Помогаю экспертам делать миллионные запуски в&nbsp;социальных сетях</p>
    <div class="stats">
      <div class="line" {a('up', .1)}><strong><span class="cnt" data-to="150" data-suf="+">150+</span></strong><span>миллионов ₽ — столько <b>продал курсов</b> за 5&nbsp;лет</span></div>
      <div class="line" {a('up', .2)}><strong><span class="cnt" data-to="40" data-suf="+">40+</span></strong><span><b>Обучил учеников</b> по запускам</span></div>
      <div class="line" {a('up', .3)}><strong style="font-size:clamp(34px,3.2vw,64px)">Тимочко</strong><span>Работал с <b>Михаилом Тимочко</b> (блогер-миллионник)</span></div>
    </div>
    <div class="cta" {a('up', .4)}>{link(CHANNEL, 'Подписаться на канал', 'go')}<p>Мой экспертный Telegram-канал про запуски</p></div>
  </div>
  <div class="photos">
    <div class="phw phw1 fl"><div class="ph" {a('rev', .1)}>{img('p02_X8.jpg')}</div></div>
    <div class="phw phw2 fl" style="animation-delay:-2s"><div class="ph" {a('rev', .25)}>{img('p02_X9.jpg')}</div></div>
    <div class="phw phw3 fl" style="animation-delay:-4s"><div class="ph" {a('rev', .4)}>{img('p02_X10.jpg')}</div></div>
  </div>
</div>''', 'about', '78%', '40%')

# ---------------------------------------------------------------- ПРОЕКТЫ
cards = ''
for k, c in enumerate(cases):
    st = c['sumtxt'].replace(' ₽', '<i>&nbsp;₽</i>')
    cards += '<a class="it card" href="#%s" %s><small><span>Кейс <b>%02d</b></span><span>→</span></small><div><h3>%s</h3></div><div class="sum">%s<span>%s</span></div></a>' % (
        c['id'], a('up', (k % 3) * .08), c['n'], esc(c['short']), st, esc(c['sumnote']))
section('projects', 'Мои проекты', f'''
<div class="kicker">Вот мои проекты</div>
<div style="margin-top:14px">{hd(['Мои <em>проекты</em>'], 'l')}</div>
<div class="pg">{cards}</div>''', 'proj', '50%', '60%')

# ---------------------------------------------------------------- КЕЙСЫ
for c in cases:
    num = '%02d' % c['n']
    if c.get('sum'):
        metric = '<div class="num"><span class="cnt" data-to="%d">%s</span><i>&nbsp;₽</i></div>' % (c['sum'], money(c['sum']))
    else:
        metric = '<div class="num t">%s</div>' % c['sumtxt_big'].replace('₽', '<i>₽</i>')
    reach = '<div class="reach"><small>Охваты</small><b>%s</b></div>' % money(c['reach']) if c.get('reach') else ''
    sub = '<div class="cap sumsub" %s>%s</div>' % (a('up', .3), esc(c['sumsub'])) if c.get('sumsub') else ''
    links = ''
    if c.get('href'):
        links = '<div class="links" %s>%s</div>' % (a('up', .3), link(c['href'], c['hlabel'], 'lk solid' if c.get('hsolid') else 'lk'))
    right = ''
    if c.get('det'):
        right += '<div class="blk" %s><h4>Подробности</h4><p>%s</p></div>' % (a('up', .1), esc(c['det']))
    if c.get('was'):
        right += '<div class="blk" %s><h4>Что было</h4><ul>%s</ul></div>' % (a('up', .1), ''.join('<li>%s</li>' % esc(x) for x in c['was']))
    if c.get('did'):
        right += '<div class="blk" %s><h4>Что я делал</h4><ul>%s</ul></div>' % (a('up', .2), ''.join('<li>%s</li>' % esc(x) for x in c['did']))
    gcards = ''
    # карточки с кнопкой-ссылкой идут первыми в ряду, видеоотзывы в конце
    gal = sorted(c['gal'], key=lambda x: 0 if x.get('hl') else (2 if x.get('rev') else 1))
    for k, cd in enumerate(gal):
        d = .05 + k * .1
        if cd.get('rev'):
            gcards += '''<div class="gcard card rev" style="--r:1" %s>
  <div class="gi" style="--r:1"><a class="circ" href="%s" target="_blank" rel="noopener noreferrer">%s<span class="play"></span></a></div>
  <div class="cap">%s</div>%s</div>''' % (a('rev', d), cd['href'], img(cd['rev']), esc(cd['cap']), link(cd['href'], 'Смотреть отзыв'))
        else:
            rs = [ratio(x) for x in cd['img']]
            r = sum(rs)
            ims = ''.join(img(x, extra=' style="--f:%.3f"' % q) for x, q in zip(cd['img'], rs))
            lk = link(cd['href'], cd.get('hl', 'Открыть')) if cd.get('href') else ''
            gcards += '''<div class="gcard card" style="--r:%.3f" %s>
  <div class="gi%s" style="--r:%.3f">%s</div>
  <div class="row"><div class="cap">%s</div>%s</div></div>''' % (r, a('rev', d), ' multi' if cd.get('multi') else '', r, ims, esc(cd['cap']), lk)
    one = ' one' if len(c['gal']) == 1 else ''
    section(c['id'], 'Кейс ' + num, f'''
<div class="ctop">
  <div>
    <div class="kicker"><b>Кейс {num}</b> · {esc(c['tag'])}</div>
    {hd(c['lines'], 'l', .05)}
    <div class="metric" {a('up', .2)}><div><small>{esc(c['sumlabel'])}</small>{metric}</div>{reach}</div>
    {sub}{links}
  </div>
  <div class="cr">{right}</div>
</div>
<div class="gal{one}">{gcards}</div>''', 'case', '30%', '45%', bignum=num)

# ---------------------------------------------------------------- ОТЗЫВЫ И РЕЗУЛЬТАТЫ
rev_imgs = ['p33_X87.jpg', 'p33_X88.jpg', 'p33_X89.jpg', 'p33_X90.jpg', 'p33_X91.jpg']
row = ''.join('<a href="%s" target="_blank" rel="noopener noreferrer" tabindex="-1">%s</a>' % (REVIEWS, img(x, alt='Отзыв')) for x in rev_imgs * 2)
section('reviews', 'Отзывы', f'''
<div class="kicker"><b>Отзывы</b></div>
<div style="margin-top:14px">{hd(['Отзывы моих', '<em>учеников и клиентов</em>'], 'm')}</div>
<div class="mq" {a('fade' if False else 'up', .2)}><div class="row">{row}</div></div>
<div class="btm" {a('up', .2)}>{link(REVIEWS, 'Все отзывы в Telegram', 'go')}</div>''', 'reviews', '50%', '60%')

order = [('p34_X95.jpg', 'Запуск на 720.000₽ + фикс 90.000₽'), ('p34_X94.jpg', 'Закрыл 2-х экспертов по 50.000₽'),
         ('p34_X96.jpg', 'Запуск на 1.600.000₽ + фикс 30.000₽'), ('p34_X92.jpg', 'Запуск на 830.000₽ в 17 лет'),
         ('p34_X93.jpg', 'Запуск на 400.000₽ + фикс 50.000₽')]
ws = ''.join('<div class="w" %s><div class="c">%s</div><span class="pill">%s</span></div>' % (a('z', k * .1), img(im), esc(cap)) for k, (im, cap) in enumerate(order))
section('wins', 'Результаты учеников', f'''
<div class="kicker"><b>Результаты</b> · ученики</div>
<div style="margin-top:14px">{hd(['Результаты', '<em>учеников</em>'], 'm')}</div>
<div class="wg">{ws}</div>''', 'wins', '50%', '60%')

# ---------------------------------------------------------------- ПРОЦЕСС
stp = ''
for n, t, txt, im, cap, note in steps:
    parts = t.split(' ')
    if t == 'Контент-план и внедрение контекста':
        title = 'Контент-план и&nbsp;внедрение <em>контекста</em>'
    else:
        title = ' '.join(parts[:-1]) + (' ' if len(parts) > 1 else '') + '<em>%s</em>' % parts[-1]
    nt = '<span class="note">%s</span>' % esc(note) if note else ''
    stp += '''<div class="stp"><div class="no" %s>%02d</div>
<div><h3 %s>%s</h3><p class="tx" %s>%s</p>%s</div>
<figure class="card" %s>%s<figcaption class="cap">%s</figcaption></figure></div>''' % (
        a('up', .05), n, a('up', .1), title, a('up', .2), txt, nt, a('rev', .15), img(im), esc(cap))
section('process', 'Как я делаю запуски', f'''
<div class="kicker"><b>Процесс</b> · 7 шагов</div>
<div style="margin-top:14px">{hd(['Как я делаю', '<em>запуски?</em>'], 'xl')}</div>
<div style="height:clamp(30px,4vw,70px)"></div>
{stp}''', 'proc', '50%', '30%')

section('details', 'Детали', f'''
<div class="wrap">
  <div>
    <div class="kicker"><b>Детали</b></div>
    <div style="margin-top:14px">{hd(['Это общими', '<em>мазками</em>'], 'l')}</div>
    <p class="lead" {a('up', .3)}>Есть ещё 100 всяких деталей, например:</p>
    <ol class="ol">
      <li {a('l', .05)}>Сайты, упаковка</li><li {a('l', .1)}>Настройка GetCourse</li><li {a('l', .15)}>Подключение кассы</li>
      <li {a('l', .2)}>Подбор специалистов</li><li {a('l', .25)}>И многое другое…</li>
    </ol>
  </div>
  <div class="note card" {a('rev', .2)}><small>Для тебя</small><p>Я возьму это <em>на себя</em>, так что пока тебя в них не погружаю</p></div>
</div>''', 'mazki', '80%', '60%')

nodes = ['Анализ ЦА и конкурентов', 'Распаковка личности и экспертности', 'Контент-план', 'Прототип продукта', 'Прогрев', 'Вебинар', 'Продажи']
lis = ''.join('<li %s><span class="num">%d</span><span class="dt"></span><small>Шаг %d</small><h3>%s</h3></li>' % (a('up', k * .12), k + 1, k + 1, esc(t)) for k, t in enumerate(nodes))
section('path', 'Весь путь запуска', f'''
<div class="kicker"><b>Путь</b> · общими мазками</div>
<div style="margin-top:14px">{hd(['Весь путь <em>запуска</em>'], 'l')}</div>
<ol>{lis}</ol>''', 'path', '50%', '60%')

# ---------------------------------------------------------------- ОБО МНЕ 2
section('me', 'Коротко обо мне', f'''
<div class="grid">
  <div class="col">
    <div class="kicker"><b>Коротко</b> обо мне</div>
    <div style="margin-top:14px">{hd(['Виталий,', '<em>Москва</em>'], 'm')}</div>
    <div class="line" {a('l', .1)}><small>Сейчас</small><strong>Наставник и продюсер онлайн-школ</strong></div>
    <div class="line" {a('l', .2)}><small>Путь</small><strong>3 года работал таргетологом, 5 лет в запусках</strong></div>
    <div class="line" {a('l', .3)}><small>Люблю</small><strong>шахматы и большой теннис</strong></div>
  </div>
  <img class="fig" src="assets/img/portrait.png" width="541" height="950" alt="" loading="lazy" {a('z', .15)}>
  <div class="col">
    <div class="kicker">Главные ценности в работе</div>
    <div style="margin-top:14px">{hd(['Мои', '<em>ценности</em>'], 'm')}</div>
    <div class="line" {a('r', .1)}><strong>Полная вовлечённость с двух сторон</strong></div>
    <div class="line" {a('r', .2)}><strong>Не терплю посредственность</strong></div>
    <div class="line" {a('r', .3)}><strong>Всегда довожу дела до конца</strong></div>
    <div class="line" {a('r', .4)}><strong>Стараюсь делать больше, чем обещаю</strong></div>
  </div>
</div>''', 'me', '50%', '70%')

section('long', 'Сотрудничество', f'''
<div class="kicker"><b>Сотрудничество</b></div>
<div style="margin-top:14px">{hd(['Нацелен на', '<em>долгосрочное</em>', 'сотрудничество'], 'xl')}</div>
<div class="box">
  <div class="card" {a('up', .1)}><small>Если не сработаемся</small><p>Сразу прямо об этом скажу</p></div>
  <div class="card" {a('up', .25)}><small>Если сойдёмся</small><p>Сделаем ещё <span class="hot">10 запусков</span></p></div>
</div>''', 'long', '50%', '70%')

section('audit', 'Начало работы', f'''
<div class="kicker"><b>Начало работы</b> · 60-минутный созвон</div>
<div style="margin-top:14px">{hd(['Начинаю работу', 'с <em>аудита</em>'], 'l')}</div>
<div class="ag">
  <div class="card" {a('up', 0)}><small>01</small><h3>Точка А</h3><p>Определяем: охваты, вовлечённость, заинтересованность аудитории в теме.</p></div>
  <div class="card" {a('up', .1)}><small>02</small><h3>Продукт</h3><p>Разбираем: что продаём, кому, какие цены, что входит.</p></div>
  <div class="card" {a('up', .2)}><small>03</small><h3>Цель</h3><p>Определяем цель: сколько хотим продать.</p></div>
  <div class="card" {a('up', .3)}><small>04</small><h3>План</h3><p>Составляем общий план прогрева.</p></div>
</div>''', 'audit', '50%', '70%')

section('contact', 'Контакты', f'''
<div class="fin">
  <div class="kicker"><b>Контакты</b></div>
  <div style="margin-top:14px">{hd(['Если интересно,', 'предлагаю <em>созвониться</em>'], 'l')}</div>
  <p class="lead" {a('up', .3)}>Обсудим подробности и&nbsp;посмотрим, подходим&nbsp;ли друг другу.</p>
  <div class="row" {a('up', .4)}>{link(TG, 'Связаться со мной', 'go')}<p>@vitalijlugovoj в Telegram</p></div>
  <div class="soc" {a('up', .5)}>{link(CHANNEL, 'Канал про запуски')}{link(REVIEWS, 'Отзывы')}</div>
</div>
{SAFE}''', 'final', '30%', '70%')

css = open(B + '/site.css', encoding='utf8').read()
fonts = open(OUT + '/assets/fonts/fonts.css', encoding='utf8').read()
js = open(B + '/site.js', encoding='utf8').read()
fonts = fonts.replace("url(Yq6R", "url(assets/fonts/Yq6R").replace("url(rax", "url(assets/fonts/rax")

doc = '''<!DOCTYPE html>
<html lang="ru">
<head>
<script>document.documentElement.classList.add('js')</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0C0A08">
<meta name="color-scheme" content="dark">
<title>Коммерческое предложение · Виталий Луговой</title>
<meta name="description" content="Помогаю экспертам делать миллионные запуски в социальных сетях: за 5 лет продал курсов на 150+ млн ₽. Кейсы, процесс запуска и условия работы.">
<meta property="og:type" content="website">
<meta property="og:title" content="Коммерческое предложение · Виталий Луговой">
<meta property="og:description" content="Миллионные запуски для экспертов: кейсы, процесс и условия работы.">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%%3E%%3Crect width='64' height='64' rx='14' fill='%%23F2451C'/%%3E%%3Cpath d='M18 14h8v14l12-14h10L34 30l15 20H39L28 35l-2 2v13h-8z' fill='%%23fff'/%%3E%%3C/svg%%3E">
<link rel="preload" as="font" type="font/woff2" crossorigin href="assets/fonts/raxdHjafvdAIOju4GcIfJH0i7zi50X3zRtuLNiMS0d6iDr-MD5Si9NGLM2-0djON_ZuWxV3ePOw.woff2">
<style>
%s
%s
</style>
</head>
<body>
<div class="vf" aria-hidden="true"><span class="vfn"><span class="vfd"><i>01</i></span><span class="vft">Обложка</span></span><span class="vfr">Коммерческое предложение · @lugovoy.vitaliy</span><span class="vfbar"></span></div>
<div class="stick"><a href="%s" target="_blank" rel="noopener noreferrer">Обсудить запуск</a></div>
<main>
%s
</main>
<footer class="foot"><span>© Виталий Луговой · продюсер запусков</span><span><a href="%s" target="_blank" rel="noopener noreferrer">Telegram</a> · <a href="%s" target="_blank" rel="noopener noreferrer">Канал</a></span></footer>
<script>
%s
</script>
</body>
</html>
''' % (fonts, css, TG, '\n'.join(secs), TG, CHANNEL, js)
open(OUT + '/index.html', 'w', encoding='utf8').write(doc)
print('sections', len(secs), 'bytes', len(doc))
