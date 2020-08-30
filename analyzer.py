from typing import List
from production import Production
from transitions.extensions import GraphMachine as Machine
from grammar import Grammar


class Analyzer:
    def __init__(self):
        self.states: List[Production] = []
        self.state_machine = Machine(
            model=self,
            states=self.states,
            auto_transitions=False,
        )
        self.grammar = Grammar()

    def analyze(self, grammar):
        pass

    def draw(self, image_name):
        self.state_machine.get_graph().draw(image_name, prog="dot")

    def load_grammar_from_file(self, file_path: str):
        self.grammar.load_from_file(file_path)
