import numpy.random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

s = pd.read_excel("data.xlsx", sheet_name="I")

S = numpy.random.normal(s["S"].mean(), 0.75, len(s["S"]))

print(stats.kstest(s["S"], "norm", N=len(s["S"])))
print(stats.kstest(S, "norm", N=len(S)))
sns.histplot(S)
sns.histplot(s["S"], color="red")
plt.legend([stats.kstest(S, "norm", N=len(S))[0:2], stats.kstest(s["S"], "norm", N=len(s["S"]))[0:2]])
plt.show()
