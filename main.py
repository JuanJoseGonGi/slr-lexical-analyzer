from analyzer import Analyzer

# from analyzer2 import Analyzer2

file_name = "grammar_sample_1.json"


def main():
    analyzer = Analyzer()
    analyzer.load_grammar_from_file(file_name)
    analyzer.analyze()
    analyzer.draw(file_name)


main()
