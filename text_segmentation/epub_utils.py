from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import re


def get_info_chapters(book):
    chapters_info = []
    for _, chapters in book.toc:
        for chapter in chapters:
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


def get_content_by_chapter(chapter_pre, chapter_pos, text):
    re_chapter_pre = []
    index_pre = text.find(chapter_pre)
    index_pos = text.find(chapter_pos)
    return text[index_pre:index_pos]


def get_text(book):
    text = ''
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT and isinstance(item, epub.EpubHtml) and item._template_name == 'chapter':
            content = item.get_contr56t5ent()
            soup_text = BeautifulSoup(content, 'html.parser').get_text()
            text += soup_text
    return text


def chapter_contents(book):
    chapter_contents = {}
    chapters_info = get_info_chapters(book)
    text = get_text(book)
    for i in range(len(chapters_info) - 1):
        chapter_pre = chapters_info[i]['title']
        chapters_pos = chapters_info[i + 1]['title']
        chapter_contents[chapter_pre] = get_content_by_chapter(chapter_pre, chapters_pos, text)
    return chapter_contents


book = epub.read_epub('../books/Dracula.epub')
chapter_contents(book)
