class ScraperView:
    def display_success_message(self):
        print("Scraping réussi. Les données ont été exportées avec succès.")

    def display_failure_message(self):
        print("Échec du scraping. Aucune donnée disponible.")

    def display_scrapping_time(self, scraping_time):
        print(f"Le scraping a pris {scraping_time:.2f} secondes.")
