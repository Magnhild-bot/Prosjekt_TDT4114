import json

class JsonFileCreator:
    def __init__(self, data: dict, filename: str):
        self.data = data
        self.filename = filename

    def save_to_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {self.filename}")

    @staticmethod
    def data_reader(filename: str, num_items: int):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Read first {num_items} values from 'value' key:")
        return data["dataset"]["value"][:num_items]