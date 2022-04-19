import pandas as pd
import sys
import matplotlib.pyplot as plt

files_to_process = [[]
for name in sys.argv[1:]:
    df = pd.read_csv(name, sep=' ', columns['x', 'quantity'])
    df = df.groupby(['x']).mean()
    df.sort_values(df.columns[0], inplace=True)
    df.to_csv(name + "-mean.dat", sep=' ', index=False, header=False)
