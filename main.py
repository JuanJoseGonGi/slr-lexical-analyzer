from analyzer import Analyzer

file_name = "grammar_sample_3.json"


def main():
    analyzer = Analyzer()
    analyzer.load_grammar_from_file(file_name)
    analyzer.analyze()
    analyzer.draw(file_name)


main()
