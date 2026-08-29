from models import LibraryItem

class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if isinstance(item, LibraryItem):
            self.items.append(item)
        else:
            raise TypeError("Only LibraryItem instances can be added to the library.")

    def checkout(self,title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError(f"Item '{title}' was not found.")

        item.checkout()
    
    def return_item(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError(f"Item '{title}' was not found.")

        item.return_item()

    def mark_lost(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError(f"Item '{title}' was not found.")

        item.mark_lost()

    def find_by_title(self, title):
        for item in self.items:
            if item.title.lower() == title.lower():
                return item

        return None

    def list_available(self):
        return [
            item
            for item in self.items
            if item.status.value == "AVAILABLE"
        ]

    def list_all(self):
        return self.items

    def sort_items(self):
        return sorted(self.items)
        
    