import token

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tok_buff = []
        self.index = 0
        self.row = 1
        self.column = 1
        self.iter_index = 0


    def _eof(self):
        if self.index < len(self.code):
            return False
        else:
            return True


    def _skip_white(self):
        while self._eof() is False and self._character().isspace():
            self._advance()


    def _skip_line_comment(self):
        while self._eof() is False and self._character() != "\n":
            self._advance()


    def _skip_block_comment(self):
        while self._eof() is False and (self._character() != "*" or self._peek() != "/"):
            self._advance()

        self._advance()
        self._advance()


    def _advance(self):
        if self._eof() is False:
            if self.code[self.index] == "\r":
                self.index += 1

            if self.code[self.index] == "\n":
                self.row += 1
                self.column = 1
            else:
                self.column += 1

            self.index += 1     


    def _peek(self):
        if self.index + 1 < len(self.code):
            return self.code[self.index+1]
        else:
            return ""


    def _read_string(self):
        self._advance()
        start = self.index
        while self._eof() is False and self._character() != "\"":
            self._advance()
        t = token.Token(token.Token_ID.STRING, None, self.row, self.column, self.code[start : self.index])
        self._advance()
        return t


    def _read_number(self):
        start = self.index
        if self._character() == "-" or self._character() == "+":
            self._advance()

        while self._eof() is False and (self._character().isnumeric() or self._character() == "."):
            self._advance()

        return token.Token(token.Token_ID.NUMBER, None, self.row, self.column, self.code[start : self.index])


    def _read_identifier(self):
        start = self.index
        while self._eof() is False and (self._character().isalnum() or self._character() == "_"):
            self._advance()

        return token.Token(token.Token_ID.IDENTIFIER, None, self.row, self.column, self.code[start : self.index])


    def _read_symbol(self):
        t = token.Token(token.Token_ID.SYMBOL, None, self.row, self.column, self.code[self.index : self.index+1])
        self._advance()
        return t


    def _character(self):
        return self.code[self.index]


    def _next_token(self):
        while self._eof() is False:
            if self._character().isspace():
                self._skip_white()
                continue 
            elif self._character() == "/" and self._peek() == "/":
                self._skip_line_comment()
                continue
            elif self._character() == "/" and self._peek() == "*":
                self._skip_block_comment()
                continue

            if self._character() == "(" or \
                   self._character() == ")" or \
                   self._character() == "}" or \
                   self._character() == "{":
                return self._read_symbol()
            elif self._character().isnumeric() or \
                    ((self._character() == "+" or self._character() == "." or self._character() == "-") and self._peek().isnumeric()):
                return self._read_number()
            elif self._character() == "\"":
                return self._read_string()
            elif self._character().isalpha() or (self._character() == "_" and self._peek().isalpha()):
                return self._read_identifier()
        
        return token.Token(token.Token_ID.EOF, None, self.row, self.column, None)


    def __iter__(self):
        self.iter_index = 0
        return self


    def __next__(self):
        tok = self[self.iter_index]
        self.iter_index += 1

        if tok.ID == token.Token_ID.EOF:
            raise StopIteration

        return tok


    def __getitem__(self, index):
        tok = None
        while True:
            if index < len(self.tok_buff):
                break;
            elif tok is not None and tok.ID == token.Token_ID.EOF:
                raise IndexError 

            tok = self._next_token()
            self.tok_buff.append(tok)
       
        return self.tok_buff[index]


