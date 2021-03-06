import ply.lex as lex
import src.tokens_rules as tokens_rules
from src.cmp.utils import Token


def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.lex in {"{", "}", ";"}:
            if token.lex == "}":
                indent -= 1
            print("    " * indent + " ".join(str(t.token_type) for t in pending))
            pending.clear()
            if token.lex == "{":
                indent += 1
    print(" ".join([str(t.token_type) for t in pending]))


def tokenize_cool_text(grammar, idx, string, num, data, printing=False):
    lexer = lex.lex(module=tokens_rules)

    # Give the lexer some input
    lexer.input(data)

    fixed_tokens = {
        t.Name: Token(t.Name, t)
        for t in grammar.terminals
        if t not in {idx, string, num}
    }

    tokens = []
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            tokens.append(Token("$", grammar.EOF))
            break  # No more input
        else:
            try:
                tokens.append(fixed_tokens[tok.type])
            except:
                try:  # for <=, ->, <-
                    tokens.append(fixed_tokens[tok.value])
                except:
                    if tok.type == "string":
                        tokens.append(Token(tok.value, string))
                    elif tok.type == "id":
                        tokens.append(Token(tok.value, idx))
                    else:
                        tokens.append(Token(tok.value, num))

    if printing:
        pprint_tokens(tokens)
    return tokens

