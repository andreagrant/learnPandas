#attempt to actually learn pandas
#https://www.safaribooksonline.com/library/view/python-for-data/9781449323592/ch02.html

import numpy
import pandas
import json

#%%

path='/users/agrant/Documents/UMN/python/pandas/pydata-book/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]

timeZones=[rec['tz'] for rec in records if 'tz' in rec]
#%%
#the hard way to get counts of timezones
def getCounts(sequence):
    counts={}
    for x in sequence:
        if x in counts:
            counts[x]+=1
        else:
            counts[x]=1
    return counts

counts=getCounts(timeZones)

#top 10 timezones
def topCount(countDict,n=10):
    valueKeyPairs=[(count,tz) for tz, count in countDict.items()]
    valueKeyPairs.sort()
    return valueKeyPairs[-n:]
    
topCount(counts)

#slightly easier way
from collections import Counter
counts=Counter(timeZones)
counts.most_common(10)

#%%
#now with pandas

frame = pandas.DataFrame(records)
tzCounts=frame['tz'].value_counts()

#replace missing values
cleanTZ=frame['tz'].fillna('Missing')
cleanTZ[cleanTZ=='']='Unknown'
tzCounts=cleanTZ.value_counts()

tzCounts[:10].plot(kind='barh',rot=0)

#%%
results=pandas.Series([x.split()[0] for x in frame.a.dropna()])

cframe=frame[frame.a.notnull()]
opsys=numpy.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')

byTZos=cframe.groupby(['tz',opsys])

aggCounts=byTZos.size().unstack().fillna(0)
aggCounts[:10]

indexer=aggCounts.sum(1).argsort()
indexer[:10]

countSubset=aggCounts.take(indexer)[-10:]
countSubset

countSubset.plot(kind='barh',stacked=True)

normedSubset=countSubset.div(countSubset.sum(1), axis=0)
normedSubset.plot(kind='barh',stacked=True)
