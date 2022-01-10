import requests
from bs4 import BeautifulSoup
import time
import json
from xml.dom import minidom

base_url='https://book.douban.com/top250?start='

headers = {
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44'
}

def get_response(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('Error', e.args)
        
def get_url(page):
    url = base_url+str(page)
    html = get_response(url)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.select('div#content')
    alist = content[0].find_all('a',{'class':{'nbg'}})
    for a in alist:
        yield a['href']
        
def get_data(url):
    html = get_response(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    spans = soup.select('h1 span')
    book_name = spans[0].get_text()
    book_author = ""
    book_press = ""
    book_ISBN = ""
    
    info = soup.select('div#info')
    spans = info[0].find_all('span', {'class':{'pl'}})
    for span in spans:
        if span.string == ' 作者':
            book_author = span.next_sibling.next_sibling.string
        if span.string == '作者:':
            if book_author == "":
                book_author = span.next_sibling.next_sibling.string
            
        if span.string == '出版社:':
            book_press = span.next_sibling.string.replace(" ","")
            
        if span.string == 'ISBN:':
            book_ISBN = span.next_sibling.string.replace(" ","")
        
    book_author = book_author.replace("\n", "")
    book_author = book_author.replace(" ", "")   
    return {
        'bookName' : book_name, 
        'bookAuthor' : book_author,
        'bookPress' : book_press,
        'bookISBN' : book_ISBN 
        
    }
    
def save_data(data):
    filename = 'bookList.txt'
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
    f.close()

    




if __name__ == '__main__':
   

    for i in range(10):
        page = i*25
        urls = get_url(page)
        for url in urls:
            data = get_data(url)
            #print(data)
            save_data(data)
        time.sleep(1)
        print('第' + str(i) + '完成----------------------')

# if __name__ == '__main__':
#     file_name = "booklist.json"
            
#     with open(file_name, 'w') as json_file:
#         for i in range(10):
#             page = i*25
#             urls = get_url(page)
#             for url in urls:
#                 data = get_data(url)
#                 print(data)
#                 json_str = json.dumps(data,indent=4,ensure_ascii=False)
#                 json_file.write(json_str)
#             time.sleep(1)
