from models.Scraper_models import ScrapperSiteModel
from controllers.Scraper_controllers import ScrapperSiteController
from views import ScraperView

# Créez une instance de la classe ScrapperSiteModel avec l'URL du site que vous souhaitez scraper


url = "ScrapperSiteController"
view = ScraperView()

model = ScrapperSiteModel(url)
controller = ScrapperSiteController(model, view)
controller.run()
