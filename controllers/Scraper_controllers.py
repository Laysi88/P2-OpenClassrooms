import csv
from datetime import datetime
from models import ScrapperBookModel
import time


class ScrapperBookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.model.scrappe_data()
        data_dict = self.model.get_book_data()
        if data_dict:
            title = data_dict.get("title", "book_data")
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"{title}_{current_date}.csv"
            self.export_to_csv([data_dict], filename)
            self.view.display_success_message()
        else:
            self.view.display_failure_message()

    def export_to_csv(self, data, filename):
        if data:
            with open(filename, "w", newline="") as csv_file:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)


class ScrapperCategoryController:
    def __init__(self, category_model, book_controller, view):
        self.category_model = category_model
        self.book_controller = book_controller
        self.view = view

    def run(self):
        book_urls = self.category_model.get_category_data()
        print(book_urls)
        if book_urls:
            for url in book_urls:
                book_model = ScrapperBookModel(url, self.book_controller)
                book_controller = ScrapperBookController(book_model, self.view)
                book_controller.run()
            self.display_success_message()
        else:
            self.display_failure_message()
