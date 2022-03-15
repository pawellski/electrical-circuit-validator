import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class LexicalAnalysisTool:

    def __init__(self, processed_text):
        self._tokens = []
        self._current_token = 0
        for token in self.__tokenize(processed_text):
            self._tokens.append(token)

    def __tokenize(self, processed_text):
        keywords = ['begin', 'capacitor', 'currentprobe', 'currentsource', 'diode', 'end',
                    'gnd', 'inductor', 'resistor', 'voltageprobe', 'voltagesource']
        token_specification = {
            'NUMBER':      r'[0-9]+\.?[0-9]*(?:[Ee]-?[0-9]+)?', # power number
            'ASSIGN':      r'=',                                # Assignment operator
            'CONNECTION':  r'--',                               # Connection operator
            'ID':          r'[A-Za-z0-9_]+',                    # Identifiers
            'OPEN_RB':     r'[(]',                              # Open round bracket
            'CLOSE_RB':    r'[)]',                              # Close round bracket
            'OPEN_SB':     r'[\[]',                             # Open square bracket
            'CLOSE_SB':    r'[\]]',                             # Close square bracket
            'COMMA':       r'[,]',                              # Comma
            'NEWLINE':     r'\n',                               # Line endings
            'SKIP':        r'[ \t]',                            # Skip over spaces and tabs
        }

        regex = '|'.join(f'(?P<{kind}>{pattern})' for kind, pattern in token_specification.items())
        extract_token = re.compile(regex).match
        match = extract_token(processed_text)
        line_number = 1
        current_position = line_start = 0

        while match is not None:
            kind = match.lastgroup
            if kind == 'NEWLINE':
                value = match.group(kind)
                yield Token(kind, value, line_number, match.start()-line_start)
                line_start = current_position
                line_number += 1
            elif kind != 'SKIP':
                value = match.group(kind)
                if kind == 'ID' and value in keywords:
                    kind = value.upper()
                if kind == 'NUMBER' and (value == '1' or value == '2'):
                    kind = 'INT12'
                yield Token(kind, value, line_number, match.start()-line_start)
            current_position = match.end()
            match = extract_token(processed_text, current_position)
        if current_position != len(processed_text):
            raise RuntimeError(f'Lexical analysis error: Unexpected character {processed_text[current_position]} on line {line_number} at {current_position-line_start} position')
        yield Token('EOF', '', line_number, current_position-line_start)

    def next_token(self):
        self._current_token += 1
        if self._current_token-1 < len(self._tokens):
            return self._tokens[self._current_token-1]
        else:
            return None