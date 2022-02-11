import random
import numpy.linalg
from numpy.linalg import solve as solve_out_of_the_box

acc = 3 # number of digit after dot
class Matrix:  # Re-invent the wheel
    def __init__(self, matrix: int or [[]]):
        if type(matrix) == type([[]]) and len(matrix) == len(matrix[0]) - 1:
                self.res = [i[-1] for i in matrix]
                self.les = [i[0:-1] for i in matrix]
                self.matrix = matrix
        else:
            n = matrix if type(matrix)==int else 3

            self.matrix = [[float(random.randint(-100, 100)) for k in range(n + 1)] for l in range(n)]
            self.les = [i[0:-1] for i in self.matrix]
            self.res = [i[-1] for i in self.matrix]

    def __str__(self): # just for beautiful print
        maxn = max(self.matrix[0])
        minn = min(self.matrix[0])
        for i in self.matrix:
            if maxn < max(i):
                maxn = max(i)
            if minn > min(i):
                minn = min(i)
        maxn = max(len(str(round(maxn,acc))), len(str(round(minn,acc))))
        s = ""
        minm = 0

        for i in self.matrix:
            if minm != 0:
                s += minm
            s += "⎢ "
            for j in i:
                s += str(round(j,acc)) + " " * (maxn - len(str(round(j,acc))) + 2)
            s = s[0:len(s) - maxn-3]+ " ⎢"+ s[len(s) - maxn-3:]
            if minm == 0:
                minm = "⎢" + " " * (len(s) - maxn-5) + "⎢" + " "*(maxn+1)  + " ⎢\n"
            s = s[:-2]
            s += " ⎢\n"

        return s

    def minus(self, i, j, mn=1.):
        i, j = i - 1, j - 1
        x = self.matrix[i]
        y = self.matrix[j]
        for k in range(len(self.matrix[i])):
            self.matrix[i][k] -= self.matrix[j][k] * mn

    def mult(self, i, n):
        for k in range(len(self.matrix[i - 1])):
            self.matrix[i - 1][k] *= n

    def gaus(self):
        matrix = Matrix(self.matrix)
        # forward
        for i in range(len(self.matrix)):
            if matrix[i][i] != 0:
                for j in range(i + 1, len(self.matrix)):
                    matrix.minus(j + 1, i + 1, matrix[j][i] / matrix[i][i])
        print(matrix)
        # backward
        for i in range(len(self.matrix) - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                matrix.minus(j + 1, i + 1, matrix[j][i] / matrix[i][i])
        self.matrix = matrix.matrix
        print(matrix)
        answers = []
        # last step to solution
        for i in range(len(self.matrix)):
            answers.append(self.matrix[i][len(self.matrix)] / self.matrix[i][i])
        return answers

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __getitem__(self, key):
        return self.matrix[key]

    def __iter__(self):
        return iter(self.matrix)


matrix = Matrix([[1,2,3],[4,2,5]])
print(matrix)
print(numpy.linalg.norm(numpy.array(matrix.gaus()) - solve_out_of_the_box(matrix.les, matrix.res)))

matrix = Matrix(4)
print(matrix)
print(numpy.linalg.norm(numpy.array(matrix.gaus()) - solve_out_of_the_box(matrix.les, matrix.res)))
