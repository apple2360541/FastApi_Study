class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


from pydantic import BaseModel


class ParramItem(BaseModel):
    title: str
    size: int
