import requests
from bs4 import BeautifulSoup

r = requests.get('http://books.toscrape.com/')

html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')

all_book = soup.findAll("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

books = []
for book in all_book:
    content = book.find('h3')
    data = content.a
    title = data.get('title')
    books.append(title)

lentghbooks = len(books)

print("There are", lentghbooks, "books :")
print(books)