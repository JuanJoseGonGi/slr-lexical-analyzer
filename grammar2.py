from constants import LAMBDA_SYMBOL
from typing import List, Dict
from production import Production
import json

ErrNoProductions = Exception("file does not have productions")
ErrNoTerminals = Exception("file does not have terminals")
ErrNoNoTerminals = Exception("file does not have no terminals")
ErrNoNoTerminalProductionLeft = Exception(
    "production left is not in no_terminals"
)
ErrSymbolNotDefined = Exception(
    "symbol is not defined as terminal or no_terminal"
)


class Grammar:
    def __init__(self):
        self.terminals: List[str] = []
        self.no_terminals: List[str] = []
        self.productions: List[Production] = []
        self.initial_symbol: str = ""

    def validate_loaded_file(self, loaded_json: Dict):
        if loaded_json.get("terminals") is None:
            raise ErrNoTerminals

        self.terminals = loaded_json["terminals"]
        self.terminals.append(LAMBDA_SYMBOL)

        if loaded_json.get("no_terminals") is None:
            raise ErrNoNoTerminals

        self.no_terminals = loaded_json["no_terminals"]

        if loaded_json.get("productions") is None:
            raise ErrNoProductions

        productions: Dict[str, List[List[str]]] = loaded_json["productions"]

        for production_left in productions:
            if production_left not in self.no_terminals:
                raise ErrNoNoTerminalProductionLeft
            
            if self.initial_symbol == "":
                self.initial_symbol = production_left

            for symbols in productions[production_left]:
                for symbol in symbols:
                    if (
                        symbol not in self.no_terminals
                        and symbol not in self.terminals
                    ):
                        print("Symbol:" + symbol)
                        raise ErrSymbolNotDefined

                self.productions.append(Production(production_left, symbols))

    def load_from_file(self, file_path: str):
        file = open(file_path)
        loaded_json: Dict = json.load(file)

        try:
            self.validate_loaded_file(loaded_json)
        except Exception as err:
            print(err)

    def calculate_production_set(self, production, prediction_symbol, last_prediction_set):
        if production.left == self.initial_symbol:
            production.prediction_set.append('$')
            return
        
        for produc in self.productions:
            if produc.left == prediction_symbol:
                production.prediction_set = self.calculate_first_for_production(produc, last_prediction_set)
                break


    def calculate_first_for_production(self, production, last_prediction_set):
        if production is None:
            return []

        production_first: List[str] = []
        production_temp : List[str] = []

        for symbols in production.symbols:
            if symbols[0] == LAMBDA_SYMBOL:
                for symbol in last_prediction_set:
                    if symbol not in production_first:
                        production_first.append(symbol)
            elif symbols[0] in self.terminals:
                production_first.append(symbols[0])
            elif symbols[0] in self.no_terminals:
                for produc in self.productions:
                    if produc.left == symbols[0]:
                        production_temp = self.calculate_first_for_production(produc, last_prediction_set)
                        break
                for symbol in production_temp:
                    if symbol not in production_first:
                        production_first.append(symbol)
        
        return production_first
