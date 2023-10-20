from models import ScrapperBookModel, ScrapperCategoryModel, ScrapperSiteModel
import os, csv, string
import requests, sys
from views import ScraperView


class MainController:
    def run(self):
        while True:
            choice = (
                input("Voulez-vous scraper un livre (L), une catégorie (C), le site (S) ou quitter (Q) ? ")
                .strip()
                .lower()
            )

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
            elif choice == "s":
                url = "http://books.toscrape.com/"
                view = ScraperView()
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.RequestException:
                    print(f"URL invalide ")
                    continue
                model = ScrapperSiteModel(url)
                controller = ScrapperSiteController(model, view)
                controller.run()
                sys.exit()
            elif choice == "q":
                print("Programme terminé.")
                break
            else:
                print(
                    "Choix invalide. Veuillez entrer 'L' pour scraper un livre, 'C' pour scraper une catégorie, ou 'Q' pour quitter."
                )


def clean_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c if c in valid_chars else "_" for c in filename)


class ScrapperBookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.model.scrappe_data()
        data_dict = self.model.get_book_data()
        if data_dict:
            title = data_dict.get("title", "book_data")
            cleaned_title = clean_filename(title)
            filename = f"{cleaned_title}.csv"
            image_url = data_dict.get("image_url")
            if image_url:
                script_directory = os.path.dirname(os.path.abspath(__file__))
                parent_directory = os.path.abspath(os.path.join(script_directory, os.path.pardir))
                image_directory = os.path.join(parent_directory, "Pictures")
                image_filename = os.path.join(image_directory, f"{cleaned_title}_image.jpg")
                self.download_image(image_url, image_filename)
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
                    title = book_data.get("title", "book_data")
                    cleaned_title = clean_filename(title)
                    image_url = book_data.get("image_url")
                    if image_url:
                        script_directory = os.path.dirname(os.path.abspath(__file__))
                        parent_directory = os.path.abspath(os.path.join(script_directory, os.path.pardir))
                        image_directory = os.path.join(parent_directory, "Pictures")
                        image_filename = os.path.join(image_directory, f"{cleaned_title}_image.jpg")
                        self.download_image(image_url, image_filename)
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

    def download_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as file:
                file.write(response.content)
                self.view.display_succes_image_download_message()
        else:
            self.view.display_failure_image_download_message()


class ScrapperSiteController:
    def __init__(self, site_model, view):
        self.site_model = site_model
        self.view = view

    def run(self):
        category_urls = self.site_model.get_site_data()
        if category_urls:
            for url in category_urls:
                book_category = ScrapperCategoryModel(url)
                category_data = book_category.get_category_data()
                if category_data:
                    book_data_list = []
                    current_category = None

                    for url in category_data:
                        book_model = ScrapperBookModel(url)
                        book_model.scrappe_data()
                        book_data = book_model.get_book_data()
                        if book_data:
                            book_category = book_data.get("category")

                            if current_category is None:
                                current_category = book_category
                            elif current_category != book_category:
                                csv_filename = f"{book_category}.csv"
                                self.export_to_csv(book_data_list, csv_filename)
                                current_category = book_category
                                book_data_list = []
                            print("Scrapping en cour")
                            book_data_list.append(book_data)
                            title = book_data.get("title", "book_data")
                            cleaned_title = clean_filename(title)
                            image_url = book_data.get("image_url")
                            if image_url:
                                script_directory = os.path.dirname(os.path.abspath(__file__))
                                parent_directory = os.path.abspath(os.path.join(script_directory, os.path.pardir))
                                image_directory = os.path.join(parent_directory, "Pictures")
                                image_filename = os.path.join(image_directory, f"{cleaned_title}_image.jpg")
                                self.download_image(image_url, image_filename)

                    if book_data_list:
                        csv_filename = f"{current_category}.csv"
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

    def download_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as file:
                file.write(response.content)
                self.view.display_succes_image_download_message()
        else:
            self.view.display_failure_image_download_message()
