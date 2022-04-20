import sys
import os
import re
import pandas as pd
import numpy as np
import scipy.stats


def getMeanForEachRow(df):
    s = [[]]
    for i in range(len(df.index)):
        s.append([])
        mean_CI_row = mean_confidence_interval_row(df.iloc[i].tolist())
        s[i] = mean_CI_row
    return s


def mean_confidence_interval_row(data, confidence=0.95):
    data = [float(i) for i in data]
    a = 1.0 * np.array(data)
    a = a[~np.isnan(a)]
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    print(a, m)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def appendMeanAndCI(df):
    mean_CI_rows = getMeanForEachRow(df)
    mean_CI_rows = [ele for ele in mean_CI_rows if ele != []]
    df_b = pd.DataFrame(mean_CI_rows, index=df.index, columns=['mean', 'mean-h', 'mean+h'])
    df = df.join(df_b)
    #print(df.head())
    #df = pd.concat(df, dfTemp, on='x')
    #print(df.dtypes, dfTemp.dtypes)
    #df = pd.concat(df, dfTemp)
    #ci = getCIForEachRow(df)
    return df

class DataSetProcessor:
    def __init__(self, data_sets):
        self.sorted_data = {}
        self.datatowrite = {}
        self.all_data = ()
        self.keys = ()
        self.data_sets = data_sets

    @staticmethod
    def readLinesIntoList(f, lines_no):
        l = [[float(val) for val in f.readline().split()] for i in range(lines_no)]
        return l

    def createDictEntry(self, line, data_set):
        regexes = ("^plot-z-distribution-pressure", "^plot-z-distribution-axial-velocity", 
                   "^plot-wall-distribution-wall-shear-stress")
        for regex in regexes:
            keyword = ""
            if re.search(regex,line):
                keyword=line.rstrip()
                entries_no = int(self.f.readline())
                data = self.readLinesIntoList(self.f, entries_no)
                df_b = pd.DataFrame(data, columns=['x', data_set])
                df_b = df_b.set_index('x')
                ### need to make sure we are not merging none with dataframe, so if theres is no 
                #existing dataframe we need to create one before merging
                try:
                    #print(self.sorted_data[keyword].head())
                    #print(df_b.head())
                    #print(pd.merge(self.sorted_data[keyword], df_b, on="x").head())
                    df_a = self.sorted_data[keyword]
                    self.sorted_data[keyword] = df_a.join(df_b)
                    #self.sorted_data[keyword] = df_a.join(df_b, on="x", lsuffix='_')
                    #print(self.sorted_data[keyword].head())
                except KeyError:
                    self.sorted_data[keyword] = df_b


    def sortDataSetsIntoDict(self, data_set):
        with open(data_set) as self.f:
            for line in self.f:
                self.createDictEntry(line, data_set)

            #self.all_data = pd.merge(self.all_data, self.sorted_data, on='x')

    def makeDirsForDataSets(self, data_set):
        dir_name = os.path.splitext(data_set)[0]
        self.dir_name = os.path.join('sorted_data', dir_name)
        os.makedirs(self.dir_name, exist_ok=True)

    def writeSortedDataSets(self):
        for key in self.sorted_data:
            df = self.sorted_data[key]
            file_name = os.path.join(key + ".dat")
            file_path = os.path.join(self.dir_name, file_name)
            dummy_df = df.iloc[:,-1]
            dummy_df.to_csv(file_path, sep=' ', index=True, header=False)

    def createAndWriteDict(self, data_set):
        self.sortDataSetsIntoDict(data_set)
        self.makeDirsForDataSets(data_set)
        self.writeSortedDataSets()


    def createAndWriteDicts(self):
        self.all_data_transformed = {}
        for data_set in self.data_sets:
            if os.path.isfile(data_set):
                self.createAndWriteDict(data_set)
            else:
                print(data_set, "is not a file - skipping\n")
        #self.printSortedData()

    def printSortedData(self):
        for key in self.sorted_data.keys():
            print(self.sorted_data[key].head())
    

data_sets = [sys.argv[i] for i in range(1 ,len(sys.argv))]

d = DataSetProcessor(data_sets)    
d.createAndWriteDicts()

os.makedirs("mean_CI_data", exist_ok=True)
for key in d.sorted_data.keys():
    df = d.sorted_data[key]
    df = appendMeanAndCI(df)
    filename =os.path.join("mean_CI_data", key + ".dat")
    df.to_csv(filename, columns=['mean', 'mean-h', 'mean+h'], sep=' ', index=True, header=False)


