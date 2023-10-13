from bs4 import BeautifulSoup as bs
import requests


class ScraperBookModel:
    def __init__(self, url, controller, view):
        self.url = url
        self.data = None
        self.controller = controller
        self.view = view

    def scrape_data(self):
        response = requests.get(self.url)
        html = response.content
        soup = bs(html, "lxml")
        self.data = soup

    def get_book_data(self):
        if self.data is not None:
            # Obtenir l'URL de la page du livre
            product_page_url = self.url

            # Obtenir l'UPC du livre
            universal_product_code = self.data.select_one(
                "table.table.table-striped th:-soup-contains('UPC') + td"
            ).text.strip()

            # Obtenir le titre du livre
            title = self.data.find("h1").text.strip()

            # Obtenir le prix TTC du livre
            price_including_tax = self.data.select_one(
                "table.table.table-striped th:-soup-contains('Price (incl. tax)') + td"
            ).text.strip()

            # Obtenir le prix HT du livre
            price_excluding_tax = self.data.select_one(
                "table.table.table-striped th:-soup-contains('Price (excl. tax)') + td"
            ).text.strip()

            # Obtenir le nombre de livre en stock
            number_available = self.data.select_one(
                "table.table.table-striped th:-soup-contains('Availability')+ td"
            ).text.strip()

            # Obtenir la description du livre
            product_description = self.data.select_one("#product_description + p").text.strip()

            # Obtenir la catégorie du livre
            active_li = self.data.find("li", class_="active")
            if active_li:
                category = active_li.find_previous("a").text.strip()

            # Obtenir la note du livre
            review_rating = self.data.find("p", class_="star-rating")["class"][1]

            # Obtenir l'adresse entière de l'image
            base_url = "http://books.toscrape.com/"
            image_url = self.data.select_one("div#product_gallery img")["src"]
            full_image_url = base_url + image_url[6:]

            data_dict = {
                "product_page_url": product_page_url,
                "universal_product_code": universal_product_code,
                "title": title,
                "price_including_tax": price_including_tax,
                "price_excluding_tax": price_excluding_tax,
                "number_availabitity": number_available,
                "product_description": product_description,
                "category": category,
                "review_rating": review_rating,
                "image_url": full_image_url,
            }
            return data_dict
        return None


class ScrapperCategoryModel:
    def __init__(self, category_url):
        self.base_url = "http://books.toscrape.com/catalogue/"
        self.category_url = category_url
        self.book_data_list = []

    def scrape_category_data(self):
        next_page = self.category_url

        while next_page:
            response = requests.get(next_page)
            html = response.content
            soup = bs(html, "lxml")

            h3_elements = soup.find_all("h3")

            for h3 in h3_elements:
                a_tag = h3.find("a")
                if a_tag and "href" in a_tag.attrs:
                    book_url = a_tag["href"]
                    full_url = self.base_url + book_url[9:]
                    self.book_data_list.append(full_url)

            # Trouver le lien de la page suivante (s'il existe)
            next_page_tag = soup.find("li", class_="next")
            if next_page_tag:
                next_page = self.base_url + next_page_tag.find("a")["href"]
            else:
                next_page = None

        return self.book_data_list
