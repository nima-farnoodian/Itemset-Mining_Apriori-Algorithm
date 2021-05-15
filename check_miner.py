from itemset_miner import *
import time
miner=itemset_miner('chess.dat')


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