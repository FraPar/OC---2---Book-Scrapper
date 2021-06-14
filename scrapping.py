import requests
from bs4 import BeautifulSoup
import csv

r = requests.get('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')

html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')

fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

book_infos = soup.findAll("tr")

book_upc = book_infos[0].text.replace("UPC","").strip()

book_title = soup.find("div", {"class":"col-sm-6 product_main"}).find("h1").text.strip()

book_pet = book_infos[2].text.split("£",1)[1].strip()

book_pit = book_infos[3].text.split("£",1)[1].strip()

book_avlb = book_infos[5].text.split("(",1)[1].split(" ",1)[0].strip()

book_desc = soup.findAll("p")[-1].text

book_cat = soup.findAll('li')[-2].text.strip()

book_rate = book_infos[6].text.split(" ",1)[-1].split("\n",1)[-1].strip()

book_imgurl = "https://books.toscrape.com/" + soup.findAll("img")[0]["src"].replace("../../","").strip()

book_data = [r.url, book_upc, book_title, book_pet, book_pit, book_avlb, book_desc, book_cat, book_rate, book_imgurl ]

print(fields)
#print(r.url)
#print(book_upc)
#print(book_title)
#print(book_pet)
#print(book_pit)
#print(book_avlb)
#print(book_desc)
#print(book_cat)
#print(book_rate)
#print(book_imgurl)
print(book_data)


