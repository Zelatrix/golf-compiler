class Error(Exception):
    pass

class LexerError(Error):
    pass

class ParserError(Error):
    pass

class CodeGenError(Error):
    pass

class FileNotExistsError(Error):
    pass
