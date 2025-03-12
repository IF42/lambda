from enum import Enum

class Token_ID(Enum):
    EOF = 0
    IDENTIFIER = 1
    STRING = 2
    NUMBER = 3
    SYMBOL = 4


class Token:
    def __init__(self, ID, file, row, column, text):
        self.ID = ID
        self.text = text
        self.file = file
        self.row = row
        self.column = column

    def __repr__(self):
        return f"Token (ID: {self.ID}, file: {self.file}, row: {self.row}, column: {self.column} text: \"{self.text}\")"

