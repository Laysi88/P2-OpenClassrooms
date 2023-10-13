import csv


class ScraperBookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.model.scrape_data()
        data_dict = self.model.get_book_data()
        if data_dict:
            title = data_dict.get("title", "book_data")
            filename = f"{title}.csv"
            self.export_to_csv(data_dict, filename)
            self.view.display_success_message()
        else:
            self.view.display_failure_message()

    def export_to_csv(self, data_dict, filename):
        with open(filename, "w", newline="") as csv_file:
            fieldnames = data_dict.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data_dict)
