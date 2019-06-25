from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


book = epub.read_epub('../books/Dracula.epub')

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

print(chapters_info)


# last_read = -1
# for chapter in chapters_info:
#     id = chapter['id']
#     href = chapter['href']
#     item = book.get_item_with_href(href)
#     content = str(item.get_content())
#     index = content.find(id)
#     if index == -1:
#         break
#     if last_read != -1:
#         ch = content[last_read:index]
#         print('==================================')
#         print(ch)
#     last_read = index
#
# c = 0
# for item in book.get_items():
#     if item.get_type() == ITEM_DOCUMENT and item.is_chapter():
#         # for chapter in chapters_info:
#         #     id = chapter['id']
#         #     content = str(item.get_content())
#         #     index = content.find(id)
#         #     if index == -1:
#         #         break
#         #     if last_read != -1:
#         #         ch = content[last_read:index]
#         #         print('==================================')
#         #         print(ch)
#         #     last_read = index
#
#         print('==================================')
#         print('NAME : ', item.get_name())
#         print('----------------------------------')
#         print(item.get_body_content())
#         print('----------------------------------')
#         soup = BeautifulSoup(item.get_content(), "html.parser")
#         print(soup.find('h2'))
#         print('==================================')
