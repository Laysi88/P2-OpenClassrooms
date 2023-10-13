from models import ScrapperCategoryModel
from bs4 import BeautifulSoup as bs
import time


start_time = time.time()

# URL de la catégorie que vous souhaitez scraper
category_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

# Créez une instance de la classe
scraper = ScrapperCategoryModel(category_url)

# Exécutez la méthode pour récupérer les données
book_links = scraper.scrape_category_data()

# Affichez les liens des livres récupérés
for link in book_links:
    print(link)

end_time = time.time()
elapsed_time = end_time - start_time
print("Temps d'exécution : {} secondes".format(elapsed_time))
