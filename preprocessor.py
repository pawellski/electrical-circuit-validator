class Preprocessor:
    def __init__(self, input_text):
        self._input_text = input_text
        self._processed_text = ''

    def remove_comments(self):
        for line in self._input_text.split('\n'):
            tmp_line = line
            offset = 0
            while tmp_line.startswith(' ') or tmp_line.startswith('\t'):
                tmp_line = tmp_line[1:]
                offset += 1
            idx = tmp_line.find('#')
            if idx == 0:
                continue
            elif idx != -1:
                self._processed_text += line[:idx+offset]
                self._processed_text += '\n'
            else:
                self._processed_text += line
                self._processed_text += '\n'
        return self._processed_text
