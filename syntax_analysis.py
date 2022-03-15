class SyntaxAnalysisTool:
    def __init__(self, scanner):
        self.__next_token = scanner.next_token
        self._token = self.__next_token()
        self._assign_indicator = 0
        self._connect_indicator = 0

    def __verify_token(self, token_type):
        if self._token.type != token_type:
            self.__error(f'Unexpected token: {self._token.type} | Expected token: {token_type}')
        if token_type != 'EOF':
            self._token = self.__next_token()

    def __error(self, message):
        raise RuntimeError(f'Syntax analysis error: {message}')

    ### Grammar ###
    def start(self):
        # start -> block EOF
        if self._token.type == 'NEWLINE' or self._token.type == 'BEGIN':
            self.block()
            self.__verify_token('EOF')
            print('\nFile is correct!')
        else:
            self.__error('Epsilon not allowed!')

    def block(self):
        # block -> newlines BEGIN newlines assign_statements min_one_newline connect_statement newlines END newlines
        if self._token.type == 'NEWLINE' or self._token.type == 'BEGIN':
            self.newlines()
            self.__verify_token('BEGIN')
            self.newlines()
            self.assign_statements()
            print()
            self.min_one_newline()
            self.connect_statements()
            print()
            self.newlines()
            self.__verify_token('END')
            self.newlines()
            print('Block begin...end is OK')
        else:
            self.__error('Epsilon not allowed -> [block]')
    
    def assign_statements(self):
        # assign_statements -> assign_statement assign_statements
        if self._token.type == 'ID':
            self.assign_statement()
            self.assign_statements()
        # assign_statements -> epsilon
        else:
            pass

    def assign_statement(self):
        # assign_statement -> ID ASSIGN circuit_element NEWLINE
        if self._token.type == 'ID':
            self.__verify_token('ID')
            self.__verify_token('ASSIGN')
            self.circuit_element()
            self.__verify_token('NEWLINE')
            self._assign_indicator += 1
            print(f'Assign statement {self._assign_indicator} is OK')
        else:
            self.__error('Epsilon not allowed -> [assign_statement]')

    def circuit_element(self):
        # circuit_element -> VOLTAGESOURCE OPEN_RB vcs_parameter CLOSE_RB
        if self._token.type == 'VOLTAGESOURCE':
            self.__verify_token('VOLTAGESOURCE')
            self.__verify_token('OPEN_RB')
            self.vcs_parameter()
            self.__verify_token('CLOSE_RB')
        # circuit_element -> CURRENTSOURCE OPEN_RB vcs_parameter CLOSE_RB
        elif self._token.type == 'CURRENTSOURCE':
            self.__verify_token('CURRENTSOURCE')
            self.__verify_token('OPEN_RB')
            self.vcs_parameter()
            self.__verify_token('CLOSE_RB')
        # circuit_element -> VOLTAGEPROBE OPEN_RB CLOSE_RB
        elif self._token.type == 'VOLTAGEPROBE':
            self.__verify_token('VOLTAGEPROBE')
            self.__verify_token('OPEN_RB')
            self.__verify_token('CLOSE_RB')
        # circuit_element -> CURRENTPROBE OPEN_RB CLOSE_RB
        elif self._token.type == 'CURRENTPROBE':
            self.__verify_token('CURRENTPROBE')
            self.__verify_token('OPEN_RB')
            self.__verify_token('CLOSE_RB')
        # circuit_element -> CAPACITOR OPEN_RB value CLOSE_RB
        elif self._token.type == 'CAPACITOR':
            self.__verify_token('CAPACITOR')
            self.__verify_token('OPEN_RB')
            self.value()
            self.__verify_token('CLOSE_RB')
        # circuit_element -> INDUCTOR OPEN_RB value CLOSE_RB
        elif self._token.type == 'INDUCTOR':
            self.__verify_token('INDUCTOR')
            self.__verify_token('OPEN_RB')
            self.value()
            self.__verify_token('CLOSE_RB')
        # circuit_element -> RESISTOR OPEN_RB value CLOSE_RB
        elif self._token.type == 'RESISTOR':
            self.__verify_token('RESISTOR')
            self.__verify_token('OPEN_RB')
            self.value()
            self.__verify_token('CLOSE_RB')
        # circuit_element -> DIODE OPEN_RB diode_parameters CLOSE_RB
        elif self._token.type == 'DIODE':
            self.__verify_token('DIODE')
            self.__verify_token('OPEN_RB')
            self.diode_parameters()
            self.__verify_token('CLOSE_RB')
        else:
            self.__error("Epsilon not allowed! -> [circuit_element]")
    
    def vcs_parameter(self):
        # vcs_parameter -> value
        if self._token.type == 'NUMBER' or self._token.type == 'INT12':
            self.value()
        # vcs_parameter -> epsilon
        else:
            pass

    def diode_parameters(self):
        # diode_parametrs -> ID ASSIGN value next_diode_param
        if self._token.type == 'ID':
            self.__verify_token('ID')
            self.__verify_token('ASSIGN')
            self.value()
            self.next_diode_param()
        # diode_parameter -> epsilon
        else:
            pass

    def next_diode_param(self):
        # next_diode_parameter -> COMMA diode_parameters
        if self._token.type == 'COMMA':
            self.__verify_token('COMMA')
            self.diode_parameters()
        # next_diode_parameter -> epsilon
        else:
            pass

    def value(self):
        # value -> NUMBER
        if self._token.type == 'NUMBER':
            self.__verify_token('NUMBER')
        # value -> INT12
        elif self._token.type == 'INT12':
            self.__verify_token('INT12')
        else:
            self.__error('Epsilon not allowed! -> [value]')

    def min_one_newline(self):
        # min_one_newline -> NEWLINE newlines
        if self._token.type == 'NEWLINE':
            self.__verify_token('NEWLINE')
            self.newlines()
        else:
            self.__error('Epsilon not allowed! -> [min_one_newline]')

    def newlines(self):
        # newlines -> NEWLINE newlines
        if self._token.type == 'NEWLINE':
            self.min_one_newline()
        # newlines -> epsilon
        else:
            pass

    def connect_statements(self):
        # connect_statements -> connect_statement connect_statements
        if self._token.type == 'ID' or self._token.type == 'GND':
            self.connect_statement()
            self.connect_statements()
        # connect_statements -> epsilon
        else:
            pass

    def connect_statement(self):
        # connect_statement -> first_element_pin CONNECTION element_pin NEWLINE
        if self._token.type == 'ID' or self._token.type == 'GND':
            self.first_element_pin()
            self.__verify_token('CONNECTION')
            self.element_pin()
            self.__verify_token('NEWLINE')
            self._connect_indicator += 1
            print(f'Connect statement {self._connect_indicator} is OK')
        else:
            self.__error('Epsilon not allowed! -> [connect_statement]')

    def first_element_pin(self):
        # first_element_pin -> ID OPEN_SB INT12 CLOSE_SB
        if self._token.type == 'ID':
            self.__verify_token('ID')
            self.__verify_token('OPEN_SB')
            self.__verify_token('INT12')
            self.__verify_token('CLOSE_SB')
        # first_element_pin -> GND
        elif self._token.type == 'GND':
            self.__verify_token('GND')
        else:
            self.__error('Epsilon not allowed! -> [first_element_pin]')

    def element_pin(self):
        # element_pin -> ID OPEN_SB INT12 CLOSE_SB next_element_pin
        if self._token.type == 'ID':
            self.__verify_token('ID')
            self.__verify_token('OPEN_SB')
            self.__verify_token('INT12')
            self.__verify_token('CLOSE_SB')
            self.next_element_pin()
        # element_pin -> GND next_element_pin
        elif self._token.type == 'GND':
            self.__verify_token('GND')
            self.next_element_pin()
        else:
            self.__error('Epsilon not allowed! -> [element_pin]')

    def next_element_pin(self):
        # next_element_pin -> CONNECTION element_pin
        if self._token.type == 'CONNECTION':
            self.__verify_token('CONNECTION')
            self.element_pin()
        # next_element_pin -> epsilon
        else:
            pass
