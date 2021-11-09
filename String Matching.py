from fuzzywuzzy import fuzz
import recordlinkage
import pandas as pd

def get_ratio(row):
    stringA = row[ColumnA]
    stringB = row[ColumnB]
    return fuzz.partial_ratio(stringA, stringB)

def main():
    global ColumnA, ColumnB

    RecordA = pd.read_csv('path/to/RecordA.csv') #My DataFrame A
    RecordB = pd.read_csv('path/to/RecordB.csv') #My DataFrame B
    ColumnA = 'ColumnA' # Column name that I want to match in Record A
    ColumnB = 'ColumnB' # Column name that I want to match in Record B
    cutoff = 95 # My cutoff

    indexer = recordlinkage.Index()
    indexer.full() #can be replaced with .block() or .sortedneighbourhood()
    candidate_links = indexer.index(RecordA, RecordB)
    len(candidate_links)

    multi_index = candidate_links.to_frame(index=False)
    data = pd.merge(left=multi_index, right=RecordA[ColumnA], how='inner', left_on=0, right_index=True)
    data = pd.merge(left=data, right=RecordB[ColumnB], how='inner', left_on=1, right_index=True)

    skor = data.apply(get_ratio, axis=1)

    # here i use 95 as the threshold score (of course you can alter the threshold depends on the data)
    data = data[skor>=cutoff]
    
    data

if __name__ == '__main__':
    main()