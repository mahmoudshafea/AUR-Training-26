from models import Book, DVD, Magazine,LibraryItem
from library import Library
from database import Database


def main():

    # Create library
    library = Library()

    # Create items
    book = Book(
        "Dune",
        "Frank Herbert",
        "9780441013593"
    )

    dvd = DVD(
        "Inception",
        "Christopher Nolan"
    )

    magazine = Magazine(
        "National Geographic",
        "2026-08"
    )

    # Add items
    library.add_item(book)
    library.add_item(dvd)
    library.add_item(magazine)

    print("ALL ITEMS:")
    for item in library.list_all():
        print(item)

    print("\nLOAN PERIODS:")

    for item in library.list_all():
        print(
            f"{item.title}: "
            f"{item.loan_period()} days"
        )

    print("\nCHECKING OUT DUNE:")

    library.checkout("Dune")

    print(book)

    print("\nRETURNING DUNE:")

    library.return_item("Dune")

    print(book)

    print("\nAVAILABLE ITEMS:")

    for item in library.list_available():
        print(item)

    print("\nSORTED ITEMS:")

    for item in library.sort_items():
        print(item)

    print("\nREPR:")

    print(repr(book))

    print("\nISBN VALIDATION:")

    print(
        LibraryItem.validate_isbn("9780441013593")
    )

    # Save to database
    database = Database()

    database.save(library.list_all())

    print("\nSaved to database.txt")

    # Load from database
    loaded_items = database.load()

    print("\nLOADED ITEMS:")

    for item in loaded_items:
        print(item)


if __name__ == "__main__":
    main()