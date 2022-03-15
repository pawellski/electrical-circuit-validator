import argparse
from preprocessor import Preprocessor
from lexical_analysis import LexicalAnalysisTool
from syntax_analysis import SyntaxAnalysisTool

def process_file(filename):
    if filename.endswith('.net') is False:
        print(f'Incorrect type of file: {filename}')
        exit()

    f = open(filename, 'r')
    input_text = f.read()
    f.close()

    p = Preprocessor(input_text)
    processed_text = p.remove_comments()
    try:
        scanner = LexicalAnalysisTool(processed_text)
        parser = SyntaxAnalysisTool(scanner)
        parser.start()
    except RuntimeError as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description='Parser for electrical circuit configuration files (.net format).')
    parser.add_argument('file', type=str, help="path to file which will be parsed")
    args = parser.parse_args()
    process_file(args.file)

if __name__ == '__main__':
    main()