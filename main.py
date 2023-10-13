from models import ScraperBookModel
from views import ScraperView
from controllers import ScraperBookController

url = input("Entrer l'url à scrapper : ")

model = ScraperBookModel(url, None, None)
view = ScraperView()
controller = ScraperBookController(model, view)

controller.run()
