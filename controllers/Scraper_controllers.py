import csv
from datetime import datetime
from models import ScraperBookModel
import time


class ScraperBookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.model.scrape_data()
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
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        start_time = time.time()
        book_data_list = self.model.get_category_data()
        end_time = time.time()
        if book_data_list:
            all_book_data = []
            for book_url in book_data_list:
                book_model = ScraperBookModel(book_url, self, self.view)
                book_model.scrape_data()
                data_dict = book_model.get_book_data()

                if data_dict:
                    all_book_data.append(data_dict)

            if all_book_data:
                category_name = all_book_data[0].get("category", "category_data")
                current_date = datetime.now().strftime("%Y-%m-%d")
                filename = f"{category_name}_{current_date}.csv"

                self.export_to_csv(all_book_data, filename)
                self.view.display_success_message()
            else:
                self.view.display_failure_message()
        else:
            self.view.display_failure_message()

        scrapping_time = end_time - start_time
        self.view.display_scrapping_time(scrapping_time)

    def export_to_csv(self, data_list, filename):
        with open(filename, "w", newline="") as csv_file:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for data_dict in data_list:
                writer.writerow(data_dict)
