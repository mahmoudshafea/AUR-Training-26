from models import LibraryItem
from models import LibraryItem


class Database:

    def __init__(self, filename="database.txt"):
        self.filename = filename

    def load(self):
        items = []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):

                    line = line.strip()

                    if not line:
                        continue

                    try:
                        data = self._parse_line(line)
                        item = LibraryItem.from_dict(data)
                        items.append(item)

                    except (ValueError, KeyError) as error:
                        print(
                            f"Skipping invalid line {line_number}: {error}"
                        )

        except FileNotFoundError:
            print(f"{self.filename} was not found.")
            return []

        return items

    def save(self, items):
        with open(self.filename, "w", encoding="utf-8") as file:

            for item in items:
                file.write(self._item_to_line(item) + "\n")

    @staticmethod
    def _parse_line(line):
        data = {}

        parts = line.split("|")

        for part in parts:

            if "=" not in part:
                raise ValueError("Invalid database format.")

            key, value = part.split("=", 1)

            data[key.strip()] = value.strip()

        return data

    @staticmethod
    def _item_to_line(item):

        if item.__class__.__name__ == "Book":

            return (
                f"type=Book|"
                f"title={item.title}|"
                f"author={item.author}|"
                f"isbn={item.isbn}|"
                f"status={item.status.value}"
            )

        elif item.__class__.__name__ == "DVD":

            return (
                f"type=DVD|"
                f"title={item.title}|"
                f"director={item.director}|"
                f"status={item.status.value}"
            )

        elif item.__class__.__name__ == "Magazine":

            return (
                f"type=Magazine|"
                f"title={item.title}|"
                f"issue={item.issue}|"
                f"status={item.status.value}"
            )

        raise ValueError("Unknown LibraryItem type.")