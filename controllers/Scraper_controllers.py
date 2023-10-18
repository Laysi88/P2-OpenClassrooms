import csv
from datetime import datetime
from models import ScrapperBookModel, ScrapperCategoryModel, ScrapperSiteModel
import time
import requests, sys
from views import ScraperView


class MainController:
    def run(self):
        while True:
            choice = input("Voulez-vous scraper un livre (L), une catégorie (C) ou quitter (Q) ? ").strip().lower()

            if choice == "l":
                url = input("Entrer l'url du livre à scrapper : ")
                view = ScraperView()
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.RequestException:
                    print(f"URL invalide ")
                    continue
                model = ScrapperBookModel(url)
                controller = ScrapperBookController(model, view)
                controller.run()
                sys.exit()
            elif choice == "c":
                url = input("Entrer l'url de la catégorie à scrapper : ")
                view = ScraperView()
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.RequestException:
                    print(f"URL invalide ")
                    continue
                model = ScrapperCategoryModel(url)
                controller = ScrapperCategoryController(model, view)
                controller.run()
                sys.exit()
            elif choice == "q":
                print("Programme terminé.")
                break
            else:
                print(
                    "Choix invalide. Veuillez entrer 'L' pour scraper un livre, 'C' pour scraper une catégorie, ou 'Q' pour quitter."
                )


class ScrapperBookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.model.scrappe_data()
        data_dict = self.model.get_book_data()
        if data_dict:
            title = data_dict.get("title", "book_data")
            cleaned_title = title.replace(":", "_")
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"{cleaned_title}_{current_date}.csv"
            self.export_to_csv([data_dict], filename)
            self.view.display_success_message()
        else:
            self.view.display_failure_message()

    def export_to_csv(self, data, filename):
        if data:
            with open(filename, "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)


class ScrapperCategoryController:
    def __init__(self, category_model, view):
        self.category_model = category_model
        self.view = view

    def run(self):
        book_urls = self.category_model.get_category_data()
        if book_urls:
            book_data_list = []

            for url in book_urls:
                book_model = ScrapperBookModel(url)
                book_model.scrappe_data()
                book_data = book_model.get_book_data()
                if book_data:
                    book_data_list.append(book_data)

            if book_data_list:
                category_name = book_data_list[0].get("category")
                csv_filename = f"{category_name}.csv"

                self.export_to_csv(book_data_list, csv_filename)
                self.view.display_success_message()
            else:
                self.view.display_failure_message()
        else:
            self.view.display_failure_message()

    def export_to_csv(self, data, filename):
        if data:
            with open(filename, "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)


class ScrapperSiteController:
    pass
