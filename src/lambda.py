import token
import lexer
import parser
import sys
import enum


class Dump_Opt(enum.Enum):
    DUMP_TOK = 0
    DUMP_AST = 1
    DUMP_IR = 2
    DUMP_ASM = 3


if __name__ == "__main__":
    assert len(sys.argv) > 2

    dump_opt = Dump_Opt.DUMP_AST
    infile = None
    outfile = "a.out"

    if sys.argv[1] == "dump_tok":
        dump_opt = Dump_Opt.DUMP_TOK
    elif sys.argv[1] == "dump_ast":
        dump_opt = Dump_Opt.DUMP_AST
    elif sys.argv[1] == "dump_id":
        dump_opt = Dump_Opt.DUMP_IR
    elif sys.argv[1] == "dump_asm":
        dump_opt = Dump_Opt.DUMP_ASM
    else:
        raise Exception("Unknown dump option")

    infile = sys.argv[2]

    if len(sys.argv) > 3:
        outfile = sys.argv[3]

    with open(infile, "r") as f:
        code = f.read()

    
    lex = lexer.Lexer(code)
    print(dump_opt)

    if dump_opt == Dump_Opt.DUMP_TOK:
        for t in lex:
            print(f"{t} {lex.index}")
        exit(0)

    par = parser.Parser(lex)

    print("Program exit..")
