from typing import List, Dict, Tuple
from production2 import Production
from transitions.extensions import GraphMachine as Machine
from grammar import Grammar


class Analyzer2:
    def __init__(self, type):
        self.lr0_transitions: List[Tuple[str, str]] = []
        self.lr0_states: List[str] = []
        self.lr0: Machine = None
        self.lr1: Machine = None
        self.grammar = Grammar()
        self.type = type

    def get_drawable_state(self, state: List[Production]):
        output = "\n".join([str(produ) for produ in state])

        return output

    def draw(self, name):
        self.lr0.get_graph().draw(name + ".lr0.png", prog="dot")

    def load_grammar_from_file(self, file_path: str):
        self.grammar.load_from_file(file_path)

    def analyze(self):
        if self.type == 0:
            self.generate_lr0()
        else:
            self.generate_lr1()

    def add_lr0_node(self, state):
        drawable_state = self.get_drawable_state(state)

        if drawable_state in self.lr0_states:
            return

        self.lr0.add_states(drawable_state)

    def add_lr0_edge(self, state1, state2, symbol):
        drawable_state1 = self.get_drawable_state(state1)
        drawable_state2 = self.get_drawable_state(state2)

        if (drawable_state1, drawable_state2) in self.lr0_transitions:
            return

        self.lr0_transitions.append((drawable_state1, drawable_state2))
        self.lr0.add_transition(
            trigger=symbol,
            source=drawable_state1,
            dest=drawable_state2,
        )

    def generate_lr_state_from_productions(
        self, state: List[Production]
    ) -> List[Production]:
        productions: List[Production] = self.grammar.productions
        actual_production_set: List[str] = []
        prediction_symbol = ""

        for production in state:
            if self.type == 1:
                self.grammar.calculate_production_set(production, prediction_symbol, actual_production_set)
                prediction_symbol = production.get_prediction_symbol()
                actual_production_set = production.prediction_set
            
            if production.next_symbol not in self.grammar.no_terminals:
                continue

            for produc in productions:
                if produc in state:
                    continue

                if produc.left == production.next_symbol:

                    state.append(produc)
                    continue

        return state

    def generate_lr0_states(
        self, prev_state: List[Production], seeds: List[Production], symbol
    ):
        current_state = self.generate_lr_state_from_productions(seeds.copy())
        if self.get_drawable_state(prev_state) == self.get_drawable_state(
            current_state
        ):
            return

        self.add_lr0_node(current_state)

        if len(prev_state) != 0:
            self.add_lr0_edge(prev_state, current_state, symbol)

        productions_to_analyze: Dict[str, List[Production]] = {}

        for production in current_state:
            if production.is_at_final():
                continue

            production_updated = Production(
                production.left, production.symbols
            )

            production_updated.next_symbol = production.next_symbol
            production_updated.next_symbol_index = production.next_symbol_index

            production_updated.move_to_next_symbol()

            if productions_to_analyze.get(production.next_symbol) is None:
                productions_to_analyze[production.next_symbol] = []

            productions_to_analyze[production.next_symbol].append(
                production_updated
            )

        for next_symbol in productions_to_analyze:
            self.generate_lr0_states(
                current_state, productions_to_analyze[next_symbol], next_symbol
            )

    def generate_lr0(self):
        initial_state = self.generate_lr_state_from_productions(
            [self.grammar.productions[0]]
        )

        self.lr0 = Machine(
            auto_transitions=False,
            initial=self.get_drawable_state(initial_state),
            title="LR0",
        )

        self.generate_lr0_states([], [self.grammar.productions[0]], "")

    def generate_lr1(self):
        initial_state = self.generate_lr1_state_from_productions(
            [self.grammar.productions[0]]
        )

        self.lr1 = Machine(
            auto_transitions = False,
            initial = self.get_drawable_state(initial_state),
            title = "LR1",
        )

        self.generate_lr1_states([], [self.grammar.productions[0]], "")