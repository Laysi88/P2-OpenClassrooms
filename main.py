from models import ScrapperCategoryModel, ScrapperBookModel
from views import ScraperView
from controllers import ScrapperCategoryController, ScrapperBookController

url = input("Entrer l'url à scrapper : ")
view = ScraperView()

model = ScrapperCategoryModel(url)
controller = ScrapperCategoryController(model, None, view)

controller.run()
