from models import ScraperBookModel, ScrapperCategoryModel
from views import ScraperView
from controllers import ScraperBookController, ScrapperCategoryController

choice = input("Choisissez 'book' ou 'category': ")

if choice == "book":
    # L'utilisateur veut scraper un livre spécifique
    url = input("Entrer l'url du livre à scrapper : ")
    model = ScraperBookModel(url)
    view = ScraperView()
    controller = ScraperBookController(model, view)
elif choice == "category":
    # L'utilisateur veut scraper une catégorie de livres
    category_url = input("Entrer l'url de la catégorie à scrapper : ")
    model = ScrapperCategoryModel(category_url)
    view = ScraperView()
    controller = ScrapperCategoryController(model, view)
else:
    print("Choix invalide. Veuillez choisir 'scrapbook' ou 'scrapcategory'.")

if model and view and controller:
    controller.run()
