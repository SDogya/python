from flask import Flask, render_template, request
from sympy import *
import matplotlib.pyplot as plt
import numpy as np
import os
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def welcome():
    return render_template('input_graph.html')


g = 1


@app.route('/', methods=['POST'])
def func():
    global g
    a = request.form.get("f")
    try:
        x1  = int(request.form.get("a"))
    except:
        x1=-10
    try:
        x2 = int(request.form.get("b"))
    except:
        x2 = 10
    try:
        x3 = int(request.form.get("c"))
    except:
        x3 = 100

    a = a.replace("^", "**")
    if a == "cls":
        plt.cla()
        plt.savefig(os.path.join("static", "save.png"))
    try:

        f = parse_expr(a)
        print(f == g)
        if g != f:
            s = np.linspace(x1, x2, x3)
            s1 = [f.subs({"x": i}) for i in s]
            plt.plot(s, s1)
            plt.savefig(os.path.join("static", "save.png"))
            g = f
    except:
        pass
    return render_template('input_graph.html')


if __name__ == '__main__':
    plt.savefig( os.path.join("static", "save.png"))
    app.run(debug=True)
