# Itemset-Mining_Apriori-Algorithm
In this project, for the Frequent Itemset Mining task, we have been asked to implement two itemset miners
one of which must be the Apriori algorithm, and the other one should be one of its improved versions or a
DFS based-method such as ECLAT. The aim of this project is to compare the performance of the selected
miners in terms of run-time. As our Itemset miners, we have chosen the original Apriori algorithm and
the Apriori Graph algorithm[1] that is deemed to be faster than the original one according to the authors’
claim. The Apriori Graph algorithm benefits from a O(|V | ∗ |E|) time complexity, where V and E are the set
of nodes and links of the obtained graph, respectively. Before mentioning anything about these approaches,
it is interesting to say that, in this project, we suggest the use of vertical representation proposed in ECLAT
algorithm in both aforementioned algorithms to speed up the search and candidate selection processes. We
show that, using said vertical representation, not only can these algorithms be significantly improved in terms
of run-time, but also the original Apriori algorithm could outperform the Apriori Graph algorithm so that it
can handle the largest data-set with a lower threshold within a reasonable time.

Note: Besides the original Apriori algorithm and the Apriori Graph algorithm, we also implemented a fast implementation of the eclat algorithm. See check_miner.py to realize how to work with our itemest miners.
