class ScraperView:
    def display_success_message(self):
        print("Scraping réussi. Les données ont été exportées avec succès.")

    def display_failure_message(self):
        print("Échec du scraping. Aucune donnée disponible.")

    def display_succes_image_download_message(self):
        print("Image téléchargée avec succès")

    def display_failure_image_download_message(self):
        print("Impossible de téléchargé l'image")
