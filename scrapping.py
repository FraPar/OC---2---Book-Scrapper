import requests
from bs4 import BeautifulSoup
import csv

#url we want to scrap
category = "sequential-art_5"
for i in (n+1 for n in range(1)):
    r = requests.get('https://books.toscrape.com/catalogue/category/books/' + category + '/page-' + str(i) + '.html')
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    book_in_cat = soup.findAll("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    for books in book_in_cat:
        book_to_scrap = books.find('a', href=True)
        print(book_to_scrap)
    print(len(book_in_cat))

###############OK################
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
book_desc = soup.findAll("p")[-1].text

#Category of the book
book_cat = soup.findAll('li')[-2].text.strip()

#Link image of the book
book_imgurl = "https://books.toscrape.com/" + soup.findAll("img")[0]["src"].replace("../../","").strip()

#fields of the .csv file
fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

#data fitting with fields
book_data = [r.url, book_upc, book_title, book_pet, book_pit, book_avlb, book_desc, book_cat, book_rate, book_imgurl ]

#print(fields)
#print(book_data)

#Writting in the .csv file
#with open('books.csv', 'w') as csv_file:
#    writer = csv.writer(csv_file)

#    writer.writerow(fields)
#    writer.writerow(book_data)
################################