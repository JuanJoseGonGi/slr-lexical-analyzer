from typing import List, Dict, Tuple
from production import Production
from transitions.extensions import GraphMachine as Machine
from grammar import Grammar


class Analyzer:
    def __init__(self):
        self.lr0_transitions: List[Tuple[str, str]] = []
        self.lr0_states: List[str] = []
        self.lr0: Machine = None
        self.lr1: Machine = None
        self.grammar = Grammar()

    def get_drawable_state(self, state: List[Production]) -> str:
        if len(state) == 0:
            return ""

        output = "\n".join([str(produ) for produ in state])

        if state[0].is_at_final():
            output = "R" + str(state[0].index) + "\n" + output

        return output

    def draw(self, name):
        self.lr0.get_graph().draw(name + ".lr0.png", prog="dot")

    def load_grammar_from_file(self, file_path: str):
        self.grammar.load_from_file(file_path)

    def analyze(self):
        self.generate_lr0()

    def add_lr0_node(self, state):
        drawable_state = self.get_drawable_state(state)

        if drawable_state in self.lr0_states:
            return

        self.lr0_states.append(drawable_state)

    def add_lr0_edge(self, state1, state2, symbol):
        drawable_state1 = self.get_drawable_state(state1)
        drawable_state2 = self.get_drawable_state(state2)

        if (drawable_state1, drawable_state2, symbol) in self.lr0_transitions:
            return

        self.lr0_transitions.append((drawable_state1, drawable_state2, symbol))

    def generate_lr0_state_from_productions(
        self, state: List[Production]
    ) -> List[Production]:
        productions: List[Production] = self.grammar.productions

        for production in state:
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
        current_state = self.generate_lr0_state_from_productions(seeds.copy())
        if self.get_drawable_state(prev_state) == self.get_drawable_state(
            current_state
        ):
            return

        is_analyzed = bool(
            self.get_drawable_state(current_state) in self.lr0_states
        )

        self.add_lr0_node(current_state)

        if len(prev_state) != 0:
            self.add_lr0_edge(prev_state, current_state, symbol)

        if is_analyzed:
            return

        productions_to_analyze: Dict[str, List[Production]] = {}

        for production in current_state:
            if production.is_at_final():
                continue

            production_updated = Production(
                production.left, production.symbols, production.index
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
        self.generate_lr0_states([], [self.grammar.productions[0]], "")

        initial_state = self.generate_lr0_state_from_productions(
            [self.grammar.productions[0]]
        )

        self.lr0 = Machine(
            auto_transitions=False,
            initial="Estado 0\n" + self.get_drawable_state(initial_state),
            title="LR0",
        )

        for state0, state1, symbol in self.lr0_transitions:
            state0_index = self.lr0_states.index(state0)
            state1_index = self.lr0_states.index(state1)

            self.lr0.add_transition(
                source="Estado " + str(state0_index) + "\n" + state0,
                dest="Estado " + str(state1_index) + "\n" + state1,
                trigger=symbol,
            )
