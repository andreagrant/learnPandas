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

#tzCounts[:10].plot(kind='barh',rot=0)

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

#countSubset.plot(kind='barh',stacked=True)

normedSubset=countSubset.div(countSubset.sum(1), axis=0)
normedSubset.plot(kind='barh',stacked=True)

#%%
import os
import pandas

userNames=['userID','gender','age','occupation','zip']
moviePath=path='/users/agrant/Documents/UMN/python/pandas/pydata-book/ch02/movielens/'
#moviePath=path='/Users/agrant/codes/learnPandas/pydata-book/ch02/movielens/'
thisFile=os.path.join(moviePath,'users.dat')
users=pandas.read_table(thisFile,sep='::',header=None, names=userNames,engine='python')
raterNames=['userID','movieID','rating','timestamp']
thisFile=os.path.join(moviePath,'ratings.dat')
ratings=pandas.read_table(thisFile,sep='::',header=None,names=raterNames,engine='python')
movieNames=['movieID','title','genres']
thisFile=os.path.join(moviePath,'movies.dat')
movies=pandas.read_table(thisFile,sep='::',header=None,names=movieNames,engine='python')

#%%
users[:5]
ratings[:5]
movies[:5]
ratings


#%%
#nested merge: first merge ratings+users, then merge that with movies
#pandas does the smart thing since the columns are labelled

data=pandas.merge(pandas.merge(ratings,users),movies)

#look at first row
data.ix[0]

#to get mean ratings for each film grouped by gender, use the "pivot table"
#meanRatings=data.pivot_table('rating',rows='title',cols='gender',aggfunc='mean')
#old keywords
meanRatings=data.pivot_table('rating',index='title',columns='gender',aggfunc='mean')

#AAAAAAAHHHH this is what i probably needed for the map plot!