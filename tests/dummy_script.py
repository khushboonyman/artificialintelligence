import sys
x=2500

print('DummyScript', file=sys.stdout, flush=True)
server_messages = sys.stdin
sys.setrecursionlimit(x)

commands = [
"#Domain is hospital",
"#Level name is MAExample",
"Move(W);Move(E)",
"Move(W);Move(E)",
"Move(W);Move(E)",
"Move(W);Move(E)",
"Move(W);Move(E)",
"Move(W);Move(E)",
"Move(W);Move(E)",
"Move(S);Move(N)",
"Move(S);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Move(E);NoOp",
"Push(N,N);NoOp",
"NoOp;Move(N)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Move(W)",
"NoOp;Push(S,S)"
]

for cmd in commands:
    print(cmd, file=sys.stdout, flush=True)
    response = sys.stdin.readline()
