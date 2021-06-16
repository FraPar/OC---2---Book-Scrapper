import os, csv
from scrapper.fonction import getAllCategories, getAllBooksLinksByCategories, getTreatAndSaveBookInfo
#Getting all categories of the website
cat_list = getAllCategories()

for category in cat_list:
    books_data, category_name = getAllBooksLinksByCategories(category)

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
            getTreatAndSaveBookInfo(books, file_path, category_name, writer)

    print("Successfully imported " + str(len(books_data)) + " books in the .csv")