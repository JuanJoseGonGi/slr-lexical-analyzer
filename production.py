from constants import LAMBDA_SYMBOL
from typing import List

ErrIsAtFinal = Exception("production is already at final")


class Production:
    def __init__(self, left: str, symbols: List[str], index):
        self.left = left
        self.symbols: List[str] = symbols
        self.next_symbol_index = 0
        self.next_symbol: str = self.symbols[self.next_symbol_index]
        self.prev_symbol: str = ""
        self.index = index

    def move_to_next_symbol(self):
        if self.is_at_final():
            raise ErrIsAtFinal

        self.prev_symbol = self.next_symbol
        self.next_symbol_index = self.next_symbol_index + 1

        if self.is_at_final():
            self.next_symbol = ""
            return

        self.next_symbol = self.symbols[self.next_symbol_index]

    def is_at_final(self):
        return (
            self.next_symbol_index == len(self.symbols)
            or self.next_symbol == LAMBDA_SYMBOL
        )

    def __str__(self):
        output = self.left + " -> "

        if self.is_at_final():
            return output + "".join(self.symbols) + "."

        symbols = (
            "".join(self.symbols[: self.next_symbol_index])
            + "."
            + "".join(self.symbols[self.next_symbol_index:])
        )

        return output + symbols
