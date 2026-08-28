from abc import ABC, abstractmethod
from enum import Enum

class ItemStatus(Enum):
    AVAILABLE="AVAILABLE"
    CHECKED_OUT="CHECKED_OUT"
    LOST="LOST"

class LibraryItem(ABC):
    ITEM_TYPES={}
    def __init_subclass__(cls, **kwargs):
       super().__init_subclass__(**kwargs)
       LibraryItem.ITEM_TYPES[cls.__name__] = cls
       
    def __init__(self, title,status=ItemStatus.AVAILABLE):
        self.title = title
        self._status = status
        
    @property
    def status(self):
        return self._status
    
    def checkout(self):
        if self._status!=ItemStatus.AVAILABLE:
            raise Exception(f"Item '{self.title}' is not available for checkout.")
        else:
            self._status = ItemStatus.CHECKED_OUT
            
            
    def return_item(self):
        if self._status!=ItemStatus.CHECKED_OUT:
            raise Exception(f"Item '{self.title}' is not checked out.")
        else:
            self._status = ItemStatus.AVAILABLE
            
    def mark_lost(self):
        if self._status==ItemStatus.LOST:
            raise Exception(f"Item '{self.title}' is already marked as lost.")
        else:
            self._status = ItemStatus.LOST
            
    @abstractmethod
    def loan_period(self):
        pass
    
    def __lt__(self, other):
        if not isinstance(other, LibraryItem):
            return NotImplemented

        return self.title.lower() < other.title.lower()

    def __str__(self):
        status = self.status.value.replace("_", " ").title()
        return f"{self.title} ({self.__class__.__name__}) — {status}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r}, "
            f"status={self.status.value!r})"
        )
    
    @classmethod
    def from_dict(cls, data):
        item_type = data.get("type")

        if item_type not in cls.ITEM_TYPES:
            raise ValueError(f"Unknown item type: {item_type}")

        item_class = cls.ITEM_TYPES[item_type]

        return item_class._from_dict(data)
    
    @staticmethod
    def validate_isbn(isbn):
        
        isbn = isbn.replace("-", "").replace(" ", "")

        if len(isbn) != 13 or not isbn.isdigit():
            return False

        total = 0

        for i, digit in enumerate(isbn):
            digit = int(digit)

            if i % 2 == 0:
                total += digit
            else:
                total += digit * 3

        return total % 10 == 0
    

    
class Book(LibraryItem):
    def __init__(self, title, author,isbn, status=ItemStatus.AVAILABLE):
        if not LibraryItem.validate_isbn(isbn):
            raise ValueError("Invalid ISBN-13.")
        super().__init__(title, status)
        self.author = author
        self.isbn = isbn

    def loan_period(self):
        return 21  
    
    @classmethod
    def _from_dict(cls, data):
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            status=ItemStatus[data.get("status", "AVAILABLE")]
        )
    def __repr__(self):
        return (
            f"Book("
            f"title={self.title!r}, "
            f"author={self.author!r}, "
            f"isbn={self.isbn!r}, "
            f"status={self.status.value!r})"
        )
        
class DVD(LibraryItem):
    def __init__(self, title, director, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.director = director

    def loan_period(self):
        return 5
    
    @classmethod
    def _from_dict(cls, data):
        return cls(
            title=data["title"],
            director=data["director"],
            status=ItemStatus[data.get("status", "AVAILABLE")]
        )
    
    def __repr__(self):
        return (
            f"DVD("
            f"title={self.title!r}, "
            f"director={self.director!r}, "
            f"status={self.status.value!r})"
        )

class Magazine(LibraryItem):
    def __init__(self, title, issue, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.issue= issue

    def loan_period(self):
        return 14
    
    @classmethod
    def _from_dict(cls, data):
        return cls(
            title=data["title"],
            issue_number=data["issue_number"],
            status=ItemStatus[data.get("status", "AVAILABLE")]
        )

    def __repr__(self):
        return (
            f"Magazine("
            f"title={self.title!r}, "
            f"issue_number={self.issue_number!r}, "
            f"status={self.status.value!r})"
        )