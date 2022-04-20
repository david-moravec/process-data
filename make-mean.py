import pandas as pd
import sys
import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    print("no data specified -  exiting")
    quit()

for name in sys.argv[1:]:
    df = pd.read_csv(name, sep=' ',usecols=[0, 3], names=['x', 'quantity'])
    mean = df.groupby(['x'])['x', 'quantity'].mean()
    mean.reset_index(drop=True)
    mean.to_csv("../" + name + "-mean.dat", sep=' ', index=False, header=False)
