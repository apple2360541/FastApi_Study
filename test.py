def get_full_name(first_name: str, last_name: str, age: int):
    full_name = first_name.title() + " " + last_name.title() + " age is " + str(age)
    return full_name


print(get_full_name("john", "doe", 28))
from typing import List, Set, Tuple, Dict, Optional


def process_items(items: List[str], items_t: Tuple[int, int, str], item_s: Set[bytes]):
    for item in items:
        print(item)


def process_dict(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)


def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
class Person:
    def __init__(self,name:str):
        self.name=name
def get_person_name(one_person:Person):
    return one_person.name

