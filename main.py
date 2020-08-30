from analyzer import Analyzer


def main():
    analyzer = Analyzer()
    analyzer.load_grammar_from_file("./grammar_sample_1.json")
    analyzer.draw("output.png")

    # print(analyzer.grammar.productions[0].symbols)
    # print(analyzer.grammar.productions[1].symbols)
    # print(analyzer.grammar.productions[2].symbols)
    # print(analyzer.grammar.terminals)


main()
