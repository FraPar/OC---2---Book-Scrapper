import requests
from bs4 import BeautifulSoup
import csv

#category we want to scrap
category = "historical-fiction_4"

#data of books we want to keep for scrapping
books_data = []

#setting up the loop range
prev_book_len = 0
new_book_len = prev_book_len - 1

#loop on each category of the website
print("Loading books")
for i in (n+1 for n in range(1000)):
    r = requests.get('https://books.toscrape.com/catalogue/category/books/' + category + '/page-' + str(i) + '.html')
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    book_in_cat = soup.findAll("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

    #loop on each books finded on the page, stopping while there is no more books
    if prev_book_len == new_book_len:
        break
    else :
        prev_book_len = new_book_len
        for books in book_in_cat:
            #making URL of each books to scrap
            book_to_scrap = books.find('a', href=True)["href"].replace('../../../','https://books.toscrape.com/catalogue/')
            books_data.append(book_to_scrap)
            new_book_len = len(books_data)

print(str(len(books_data)) + " books finded in " + category)

#fields of the .csv file
fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

#writting in the .csv file
with open('books.csv', 'w', newline='', encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(fields)
    for books in books_data:
        books_to_csv = []
        r = requests.get(books)

        html_doc = r.text

        soup = BeautifulSoup(html_doc, 'html.parser')

        #finding most of the informations about the book
        book_infos = soup.findAll("tr")
        book_upc = book_infos[0].text.replace("UPC","").strip()
        book_pet = book_infos[2].text.split("£",1)[1].strip()
        book_pit = book_infos[3].text.split("£",1)[1].strip()
        book_avlb = book_infos[5].text.split("(",1)[1].split(" ",1)[0].strip()
        book_rate = book_infos[6].text.split(" ",1)[-1].split("\n",1)[-1].strip()

        #Title of the book
        book_title = soup.find("div", {"class":"col-sm-6 product_main"}).find("h1").text.strip()

        #Description of the book
        book_desc = soup.find("div", {"id":"product_description"}).find_next_sibling("p").get_text().replace(";",",")
        #print(book_desc)

        #Category of the book
        book_cat = soup.findAll('li')[2].text.strip()

        #Link image of the book
        book_imgurl = "https://books.toscrape.com/" + soup.findAll("img")[0]["src"].replace("../../","").strip()

        #data fitting with fields
        books_to_csv.extend([r.url, book_upc, book_title, book_pet, book_pit, book_avlb, book_desc, book_cat, book_rate, book_imgurl])
        #print(books_to_csv)
        #print(fields)
        #print(books_to_csv)

        #Writting in the .csv file
        writer.writerow(books_to_csv)
print("Successfully imported " + str(len(books_data)) + " books in the .csv")