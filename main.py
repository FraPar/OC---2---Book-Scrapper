import requests
from bs4 import BeautifulSoup

books = []

for i in range(51):
    r = requests.get('https://books.toscrape.com/catalogue/page-'+str(i)+'.html')

    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    all_book = soup.findAll("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

    for book in all_book:
        content = book.find('h3')
        data = content.a
        title = data.get('title')
        books.append(title)

    lentghbooks = len(books)

print("There are", lentghbooks, "books :")
print(books)

with open('urls.txt', 'w') as file :
    for book in books:
        file.write(book + '\n')

#with open('urls.txt', 'r') as file :
#    for row in file:
#        print(row)


