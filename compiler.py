import lexer
import pickle

with open("wafflescript.w", "r") as f:
    c = f.read()
    l = lexer.Lexer(c)
    t = l.parse()
    ll = list(t)
    print(ll)
    with open("test.wbin", "wb+") as file:
        pickle.dump(ll, file)
    

