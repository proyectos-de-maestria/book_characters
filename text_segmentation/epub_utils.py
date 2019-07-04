from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import re
import codecs


def get_info_chapters(book):
    chapters_info = []
    # for _, chapters in book.toc:
    for chapter in book.toc:
        if hasattr(chapter, '__iter__'):
            chapter = chapter[0]
        if chapter.title.upper() != "CONTENTS":
            info = chapter.href.split('#')
            item = book.get_item_with_href(info[0])
            content = str(item.get_content())
            index = content.find(info[1])
            chapters_info.append({
                'title': chapter.title,
                'id': info[1],
                'href': info[0],
                'index': index
            })
    return chapters_info


def get_re(phrase):
    result = ''
    for word in phrase.split():
        result += word + "[ \n]+"
    return result


def get_content_by_chapter(chapter_pre, chapter_pos, text):
    re_pre = get_re(chapter_pre)
    re_pos = get_re(chapter_pos)
    index_pre = re.search(re_pre, text, flags=re.IGNORECASE).span(0)[1]
    index_pos = re.search(re_pos, text[index_pre:], flags=re.IGNORECASE).span(0)[0]

    return text[index_pre:index_pre + index_pos]


def get_text(book):
    text = ''
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT and isinstance(item, epub.EpubHtml) and item._template_name == 'chapter':
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            codetags = soup.findAll('tbody')
            if len(codetags) == 0:
                codetags = soup.findAll("blockquote")
            for codetag in codetags:
                codetag.extract()
            text += soup.get_text()
    return text


def save_text(path, book):
    path = path.replace("epub", "txt")
    file = codecs.open(path, "w", "utf-8")
    text = get_text(book)
    file.write(text)
    file.close()


def chapter_contents(book):
    chapter_contents = {}
    chapters_info = get_info_chapters(book)
    text = get_text(book)
    for i in range(len(chapters_info) - 1):
        chapter_pre = chapters_info[i]['title']
        chapters_pos = chapters_info[i + 1]['title']
        chapter_contents[chapter_pre] = get_content_by_chapter(chapter_pre, chapters_pos, text)
    return chapter_contents

