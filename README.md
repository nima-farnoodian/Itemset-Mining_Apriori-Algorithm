# Itemset Mining Algorithms (Apriori, Apriori Graph, and Eclat)

In this project, for the Frequent Itemset Mining task, we have been asked to implement two itemset miners
one of which must be the Apriori algorithm, and the other one should be one of its improved versions or a
DFS based-method such as ECLAT. The aim of this project is to compare the performance of the selected
miners in terms of run-time. As our Itemset miners for implementation, we have chosen the original Apriori algorithm and
the Apriori Graph algorithm that is deemed to be faster than the original one according to the authors’
claim. The Apriori Graph algorithm benefits from a O(|V | ∗ |E|) time complexity, where V and E are the set
of nodes and links of the obtained graph, respectively. Before mentioning anything about these approaches,
it is interesting to say that, in this project, we suggest the use of vertical representation proposed in ECLAT
algorithm in both aforementioned algorithms to speed up the search and candidate selection processes. We
show that, using said vertical representation, not only can these algorithms be significantly improved in terms
of run-time, but also the original Apriori algorithm could outperform the Apriori Graph algorithm so that it
can handle the largest data-set with a lower threshold within a reasonable time.

Note: Besides the original Apriori algorithm and the Apriori Graph algorithm, I also implemented a **fast implementation of the eclat algorithm**. See check_miner.py to realize how to work with the itemest miners.

# Report 
- You will find the report that includes the implementation details and the experimental results [here](PatternMining_Proj1.pdf).
# Dataset

Your input dataset should be of the following format:

Each line is a transaction, and each column is an item (Space deliminator). Check chess.data
```
i1 i2 i3 ...... i5
i1 i7 i1 ........ i10
...
...
...
i5 i3 i1 ... i15
```
# Usage 

``` python

from itemset_miner import *
import time
miner=itemset_miner('chess.dat') # chess is a toy dataset


startime = time.perf_counter()
ap=miner.apriori(0.6,False)
endtime = time.perf_counter()
print('Elapsed Time Apriori:', endtime-startime,'# of itemsets:',len(ap))

startime = time.perf_counter()
apg=miner.apriori_graph(0.6,False)
endtime = time.perf_counter()
print('Elapsed Time Apriori_Graph:', endtime-startime,'# of itemsets:',len(apg))


startime = time.perf_counter()
eclat=miner.eclat(0.7,False)
endtime = time.perf_counter()
print('Elapsed Time Eclat:', endtime-startime,'# of itemsets:',len(eclat))

```

Sincerely,

[Nima Farnoodian](mailto:nima.farnoodian@outlook.com)
