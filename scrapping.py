import requests
import os
from bs4 import BeautifulSoup
import csv

#Getting all categories of the website
r = requests.get('https://books.toscrape.com/catalogue/category/books_1/index.html')
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')
categories = soup.find("div", {"class":"side_categories"}).findAll("a")
#print(categories)

cat_list = []
for category in categories[1:]:
    cat_path = category.get('href').split("/")[2]
    cat_list.append(cat_path)

for category in cat_list:
    #category we want to scrap
    #category = "classics_6"
    category_name = category.split("_")[0]

    #data of books we want to keep for scrapping
    books_data = []

    #setting up the loop range
    prev_book_len = 0
    new_book_len = prev_book_len - 1

    #loop on each category of the website
    print("Loading books in " + category_name.replace("-"," "))
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

    #if there is only 1 page, the url is changing. Then we call this code
    if len(books_data) == 0:
        r = requests.get('https://books.toscrape.com/catalogue/category/books/' + category + '/index.html')
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        book_in_cat = soup.findAll("li", {"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

        #loop on each books finded on the page, stopping while there is no more books
        prev_book_len = new_book_len
        for books in book_in_cat:
            #making URL of each books to scrap
            book_to_scrap = books.find('a', href=True)["href"].replace('../../../','https://books.toscrape.com/catalogue/')
            books_data.append(book_to_scrap)
            new_book_len = len(books_data)

    print(str(len(books_data)) + " books finded in " + category_name.replace("-"," "))

    #fields of the .csv file
    fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

    #Creating Repository
    file_path = os.path.realpath(__file__).replace('scrapping.py','').replace("\\","/")
    try:
        os.makedirs(file_path + category_name, mode = 0o777, exist_ok=True)
    except FileExistsError:
        # directory already exists
        pass

    #writting in the .csv file
    with open( file_path + "/" + category_name + "/" + category_name + '_scrap.csv', 'w', newline='', encoding="utf-8") as csv_file:
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

            #Description of the book + testing if there is a description
            pre_test_desc = soup.find("div", {"id":"product_description"})
            if pre_test_desc is None:
                book_desc = "No description"
            else :
                book_desc = pre_test_desc.find_next_sibling("p").get_text().replace(";",",")

            #Category of the book
            book_cat = soup.findAll('li')[2].text.strip()

            #Link image of the book
            book_imgurl = "https://books.toscrape.com/" + soup.findAll("img")[0]["src"].replace("../../","").strip()

            #Downloading the image
            get_img = requests.get(book_imgurl)
            file = open( file_path + "/" + category_name + "/" + books.split("/")[-2] + ".png","wb")
            file.write(get_img.content)
            file.close()

            #data fitting with fields
            books_to_csv.extend([r.url, book_upc, book_title, book_pet, book_pit, book_avlb, book_desc, book_cat, book_rate, book_imgurl])
            #print(books_to_csv)
            #print(fields)
            #print(books_to_csv)

            #Writting in the .csv file
            writer.writerow(books_to_csv)

    print("Successfully imported " + str(len(books_data)) + " books in the .csv")