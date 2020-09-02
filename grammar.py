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

        productions_count = 0

        for production_left in productions:
            if production_left not in self.no_terminals:
                raise ErrNoNoTerminalProductionLeft

            for symbols in productions[production_left]:
                for symbol in symbols:
                    if (
                        symbol not in self.no_terminals
                        and symbol not in self.terminals
                    ):
                        print("Symbol:" + symbol)
                        raise ErrSymbolNotDefined

                self.productions.append(
                    Production(production_left, symbols, productions_count)
                )
                productions_count = productions_count + 1

    def load_from_file(self, file_path: str):
        file = open(file_path)
        loaded_json: Dict = json.load(file)

        try:
            self.validate_loaded_file(loaded_json)
        except Exception as err:
            print(err)
