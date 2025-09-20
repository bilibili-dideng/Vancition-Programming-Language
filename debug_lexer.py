from lexer import Lexer

source = """func main() {
    if (true) {
        System.print("if");
    } else-if (false) {
        System.print("else-if");
    }
}"""

lexer = Lexer(source)
tokens = lexer.tokenize()
for token in tokens:
    print(f'{token.type}: {token.value}')