from models import ScraperBookModel
from views import ScraperView
from controllers import ScraperController

url = input("Entrer l'url à scrapper : ")

model = ScraperBookModel(url, None, None)
view = ScraperView()
controller = ScraperController(model, view)

controller.run()
