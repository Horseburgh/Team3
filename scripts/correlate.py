import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
sbn.set()

data_dir = os.path.abspath(os.path.dirname(__file__)) + "/../data"
pddata = pd.read_csv(data_dir + "/all_data.csv", sep=',')

## Get correlation of all number columns
idf = pddata.select_dtypes(include=np.number)
idfcol = np.array(idf.columns.tolist())
icor = np.array(idf.corr())

## Get Rid of Correlated Values

mincor = .9

close = np.array([[0],[0]])

## Upper triangular so i cor j and j cor i not both present
for i in range(1, idfcol.size):
    for j in range(i+1, idfcol.size):
        if(abs(icor[i][j]) > mincor):
            ## print('%s  &  %s  :  %f' % (idfcol[i], idfcol[j], icor[i][j]))
            close = np.append(close, np.array([[i], [j]]), axis=1)

cmask = np.ones(idfcol.size)

for k in range(1, int(close.size/2)):
    t = close[0][k]
    r = close[1][k]
    if(cmask[t] == 0 or cmask[r] == 0):
        continue
    if(icor[0][r] < icor[0][t]):
        t = r
    cmask[t] = 0

## ncor stores the correlation matrix for all values that are not correlated together beyond the mincor
## ndfcol stores the name of the columns of each feature at the same index salary is index 0

ncor = icor[cmask.astype(bool),:]
ncor = ncor[:, cmask.astype(bool)]
ndfcol = idfcol[cmask.astype(bool)]

## print(ncor.shape)

## print('')

ycor = np.absolute(ncor[0,:])

## Sortcol stores the columns most correlated with salary in ascending order

sort_ind = np.argsort(ycor)
sorty = ycor[sort_ind]
sortcol = ndfcol[sort_ind]

topNum = 20     ## Most correlated values with Salary

# print('Top Correlated Number Cols to Salary')
# for n in range(2,topNum+2):
#    print('COL: %s' % (sortcol[-1*n]))

ncols = []
for n in range(2,topNum+2):
   ncols.append(sortcol[-1*n])

npnew = idf.to_numpy()
npcut = npnew[:, cmask.astype(bool)]
npsort = npcut[:, sort_ind]

## npout stores numpy array of output
npoutf = npsort[:, -1*topNum - 1:-1]
npout = np.flip(npoutf,1)
ncols.insert(0, 'Salary')

salaries = (pddata["Salary"].to_numpy()).reshape(874, 1)
new_data = pd.DataFrame(np.hstack([salaries, npout]), columns=ncols)

new_data.to_csv(data_dir+"/clean_data.csv", encoding='utf-8')
