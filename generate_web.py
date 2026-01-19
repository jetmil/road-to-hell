"""
Генератор HTML-страниц для книги "Путь в АД"
Конвертирует Markdown главы в HTML с уникальным дизайном
"""

import os
import re
from pathlib import Path

# Конфигурация
CHAPTERS_MD = Path(r"C:\Users\PC\road-to-hell\chapters")
CHAPTERS_HTML = Path(r"C:\Users\PC\road-to-hell\web-chapters")
CHAPTERS_HTML.mkdir(exist_ok=True)

# Метаданные глав
CHAPTERS = [
    {"num": "01", "file": "01-zero-trust.md", "title": "Zero Trust к собственной памяти", "part": "I"},
    {"num": "02", "file": "02-echo-chamber.md", "title": "Эхо-камера вместо фильтра", "part": "I"},
    {"num": "03", "file": "03-cowardice.md", "title": "Трусость под маской скромности", "part": "I"},
    {"num": "04", "file": "04-sincerity-negativity.md", "title": "Искренность = негатив", "part": "I"},
    {"num": "05", "file": "05-philosophy-defense.md", "title": "Философские конструкции как защита", "part": "I"},
    {"num": "06", "file": "06-thats-all-for-today.md", "title": '"На сегодня всё?"', "part": "II"},
    {"num": "07", "file": "07-test-vs-reality.md", "title": "Тест vs Реальность", "part": "II"},
    {"num": "08", "file": "08-never-vs-always-surrender.md", "title": "Никогда не сдаваться vs Всегда сдаваться", "part": "II"},
    {"num": "09", "file": "09-account-as-testament.md", "title": "Аккаунт как завещание", "part": "III"},
    {"num": "10", "file": "10-this-too-shall-pass.md", "title": "И это тоже пройдёт", "part": "III"},
    {"num": "11", "file": "11-triple-pass.md", "title": "Трёхкратный проход", "part": "IV"},
    {"num": "12", "file": "12-listen-to-unsaid.md", "title": "Слушай что не сказано", "part": "IV"},
    {"num": "13", "file": "13-when-hit-dance.md", "title": "Когда бьют — танцуй", "part": "IV"},
    {"num": "14", "file": "14-break-when-you-feel.md", "title": "Нарушай когда чуешь что надо", "part": "V"},
    {"num": "15", "file": "15-filter-not-echo.md", "title": "Фильтр, не эхо-камера", "part": "V"},
]

PART_NAMES = {
    "I": "Механизмы распада",
    "II": "Точки слома",
    "III": "Наследие распада",
    "IV": "Инструменты распознавания",
    "V": "Выход из АДа?"
}


def md_to_html_content(md_text):
    """Конвертация Markdown в HTML"""
    html = md_text

    # Убираем заголовок первого уровня (он будет в header)
    html = re.sub(r'^# .+\n', '', html)

    # Эпиграф (> *"текст"*)
    def format_epigraph(match):
        text = match.group(1).strip('*"')
        return f'<div class="epigraph decay">{text}</div>'
    html = re.sub(r'^> \*(.+?)\*$', format_epigraph, html, flags=re.MULTILINE)

    # Горизонтальные линии -> fracture
    html = re.sub(r'^---+$', '<div class="fracture"></div>', html, flags=re.MULTILINE)

    # Заголовки h2
    html = re.sub(r'^## (.+)$', r'<h2 class="fade-in">\1</h2>', html, flags=re.MULTILINE)

    # Заголовки h3
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Жирный текст
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Курсив
    html = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', html)

    # Списки
    def format_list(match):
        items = match.group(0)
        list_items = re.findall(r'^[-*] (.+)$', items, re.MULTILINE)
        if list_items:
            items_html = '\n'.join(f'<li>{item}</li>' for item in list_items)
            return f'<ul class="fade-in">\n{items_html}\n</ul>'
        return items
    html = re.sub(r'(^[-*] .+$\n?)+', format_list, html, flags=re.MULTILINE)

    # Нумерованные списки
    def format_ol(match):
        items = match.group(0)
        list_items = re.findall(r'^\d+\. (.+)$', items, re.MULTILINE)
        if list_items:
            items_html = '\n'.join(f'<li>{item}</li>' for item in list_items)
            return f'<ol class="fade-in">\n{items_html}\n</ol>'
        return items
    html = re.sub(r'(^\d+\. .+$\n?)+', format_ol, html, flags=re.MULTILINE)

    # Таблицы
    def format_table(match):
        table_text = match.group(0)
        lines = [l.strip() for l in table_text.strip().split('\n') if l.strip()]

        # Пропускаем разделитель
        header_line = lines[0]
        data_lines = [l for l in lines[2:] if not re.match(r'^[\|\-\s:]+$', l)]

        headers = [h.strip() for h in header_line.split('|') if h.strip()]
        header_html = ''.join(f'<th>{h}</th>' for h in headers)

        rows_html = ''
        for line in data_lines:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            cells_html = ''.join(f'<td>{c}</td>' for c in cells)
            rows_html += f'<tr>{cells_html}</tr>\n'

        return f'''<table class="fade-in">
<thead><tr>{header_html}</tr></thead>
<tbody>{rows_html}</tbody>
</table>'''

    html = re.sub(r'(\|.+\|\n)+', format_table, html)

    # Цитаты (blockquote) - не эпиграфы
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Параграфы
    paragraphs = []
    current_p = []
    in_special = False

    for line in html.split('\n'):
        stripped = line.strip()

        # Пропускаем пустые строки
        if not stripped:
            if current_p:
                paragraphs.append('<p class="fade-in">' + ' '.join(current_p) + '</p>')
                current_p = []
            continue

        # Проверяем специальные элементы
        if stripped.startswith('<') or stripped.startswith('#'):
            if current_p:
                paragraphs.append('<p class="fade-in">' + ' '.join(current_p) + '</p>')
                current_p = []
            paragraphs.append(stripped)
        else:
            current_p.append(stripped)

    if current_p:
        paragraphs.append('<p class="fade-in">' + ' '.join(current_p) + '</p>')

    html = '\n\n'.join(paragraphs)

    # Добавляем ember-text к ключевым словам
    keywords = ['АД', 'катастрофа', 'тюрьма', 'смерть', 'ловушка', 'опасность', 'распад']
    for kw in keywords:
        html = re.sub(rf'\b({kw})\b', r'<span class="ember-text">\1</span>', html, flags=re.IGNORECASE)

    return html


def generate_chapter_html(chapter, prev_ch, next_ch):
    """Генерация HTML страницы главы"""

    md_path = CHAPTERS_MD / chapter["file"]
    if not md_path.exists():
        print(f"SKIP: {md_path} not found")
        return None

    md_content = md_path.read_text(encoding='utf-8')

    # Извлекаем эпиграф
    epigraph_match = re.search(r'^> \*"(.+?)"\*', md_content, re.MULTILINE)
    epigraph = epigraph_match.group(1) if epigraph_match else ""

    # Убираем эпиграф из контента (он уже в header)
    content_without_epigraph = re.sub(r'^> \*".+?"\*\n*', '', md_content, flags=re.MULTILINE)

    # Конвертируем контент
    html_content = md_to_html_content(content_without_epigraph)

    # Навигация
    prev_link = ""
    next_link = ""
    if prev_ch:
        prev_link = f'<a href="{prev_ch["num"]}.html" class="nav-link nav-link--prev">{prev_ch["title"]}</a>'
    else:
        prev_link = '<a href="../index.html" class="nav-link nav-link--prev">Оглавление</a>'

    if next_ch:
        next_link = f'<a href="{next_ch["num"]}.html" class="nav-link nav-link--next">{next_ch["title"]}</a>'
    else:
        next_link = '<a href="../index.html" class="nav-link nav-link--next">Оглавление</a>'

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Глава {chapter["num"]}: {chapter["title"]} — Путь в АД">
    <title>Глава {chapter["num"]}. {chapter["title"]} — Путь в АД</title>

    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/effects.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔥</text></svg>">
</head>
<body>
    <!-- Background Effects -->
    <div class="noise"></div>
    <div class="scanlines"></div>
    <div class="vignette"></div>

    <!-- Ember Particles -->
    <div class="ember-particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>

    <!-- Depth Indicator -->
    <div class="depth-indicator"></div>
    <div class="depth-label">ГЛАВА {chapter["num"]}</div>

    <!-- Navigation -->
    <nav class="nav-main">
        <a href="../index.html" class="nav-link">◆ Оглавление</a>
    </nav>

    <!-- Chapter -->
    <article class="chapter container">
        <header class="chapter__header burn-in">
            <span class="chapter__number">Часть {chapter["part"]}. {PART_NAMES[chapter["part"]]}</span>
            <h1 class="chapter__title">{chapter["title"]}</h1>
            {f'<div class="epigraph decay">{epigraph}</div>' if epigraph else ''}
        </header>

        <!-- Chapter Illustration -->
        <figure class="chapter__illustration fade-in">
            <img src="../images/chapter_{chapter["num"]}.png" alt="{chapter["title"]}" class="chapter__img" loading="lazy">
        </figure>

        <div class="chapter__content">
            {html_content}
        </div>

        <!-- Chapter Navigation -->
        <nav class="nav-chapters">
            {prev_link}
            {next_link}
        </nav>
    </article>

    <!-- Footer -->
    <footer class="footer container">
        <p class="footer__quote">
            גם זה יעבור
            <span class="footer__quote-source">И это тоже пройдёт</span>
        </p>
    </footer>

    <script src="../js/effects.js"></script>
</body>
</html>'''

    return html


def main():
    print("=" * 50)
    print("Generating web pages for 'Road to Hell'")
    print("=" * 50)

    success = 0
    failed = 0

    for i, chapter in enumerate(CHAPTERS):
        prev_ch = CHAPTERS[i - 1] if i > 0 else None
        next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None

        html = generate_chapter_html(chapter, prev_ch, next_ch)

        if html:
            output_path = CHAPTERS_HTML / f'{chapter["num"]}.html'
            output_path.write_text(html, encoding='utf-8')
            print(f"[OK] Glava {chapter['num']}: {chapter['title']}")
            success += 1
        else:
            print(f"[ERR] Glava {chapter['num']}: ERROR")
            failed += 1

    print("=" * 50)
    print(f"Done: {success} success, {failed} errors")
    print(f"Files in: {CHAPTERS_HTML}")


if __name__ == "__main__":
    main()
