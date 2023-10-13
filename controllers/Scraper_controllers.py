class ScraperController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.model.scrape_data()
        data = self.model.get_book_data()
        self.view.display_data(data)
