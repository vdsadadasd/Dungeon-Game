import random

class Items:
    def __init__(self, name, type, quantity):
        self.name = name
        self.type = type
        self.quantity = int(quantity)
        self.row = None
        self.col = None
