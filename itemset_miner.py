""" 
Author: Nima Farnoodian
École polytechnique de Louvain, UCLouvain,  Belgium.
nima.farnoodian@student.uclouvain.be or nima.farnoodian@outlook.com.
March 19, 2021.
"""

from collections import defaultdict
from itertools import combinations

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """
        It reads the dataset file and initializes files
        Each line of the File is deemed as a transaction. 
        Each transaction in the file must include the items separated by space ' '. 
        """
        self.transactions = list()
        self.items = set()
        self.Freq_Items={}
        self.Vertical_Rep={}
        try:

            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            i=0
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(frozenset([item]))
                    if frozenset([item]) not in self.Vertical_Rep:
                        self.Vertical_Rep[frozenset([item])]=set()
                    self.Vertical_Rep[frozenset([item])].add(i)                                 
                                                                  
                    if item not in self.Freq_Items:
                        self.Freq_Items[item]=1
                    else:
                        self.Freq_Items[item]+=1
                i+=1
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def items_num(self):
        """Returns the number of different items in the dataset"""
        return len(self.items)

    def get_transaction(self, i):
        """Returns the transaction at index i as an int array"""
        return self.transactions[i]
    def get_items(self):
        return self.items
    def get_freq_items(self,minSup):
        """ Returns a list of the frequent items"""
        TrNo=len(self.transactions)
        AboveFreq=[i for i in self.Freq_Items if (self.Freq_Items[i]/TrNo)>=minSup]
        return AboveFreq
    
    def get_freq_Vertical_Rep(self,minSup):
        """ Returns the vertical representation of the frequent items"""
        if minSup!=None:
            TrNo=self.items_num()
            High_freq=self.get_freq_items(minSup)
            Vertical_Rep_high={}
            for it in High_freq:
                Vertical_Rep_high[frozenset([it])]=self.Vertical_Rep[frozenset([it])]
        return Vertical_Rep_high


class itemset_miner:
    def __init__(self, filepath):
        self.__data=Dataset(filepath)

    def __vertical_intersect(self,Vertical_rep_frequent,result_list):
    # it optimizes the apriori algorithm by more than 4x
        fixed=result_list[0]
        intersect=Vertical_rep_frequent.get(frozenset({fixed}),set())
        for i in result_list:
            intersect=intersect.intersection(Vertical_rep_frequent.get(frozenset({i}),set()))
            if len(intersect)==0:
                break  
        return intersect
    
    # Apriori Algorithm
    
    def __Pruning(self,candidateSet, prevFreqSet, length):
        tempCandidateSet = candidateSet.copy()
        for item in candidateSet:
            subsets = combinations(item, length)
            for subset in subsets:        
                if(frozenset(subset) not in prevFreqSet):# removing the set the subsets of which are not frequent 
                    tempCandidateSet.remove(item)
                    break
        return tempCandidateSet
    
    def __FindEligimateItemSet(self,itemSet, transactions, minSup, Itemsets,Vertical_rep_frequent):
        freqItemSet = set()
        # the following code is used for optimizing the searching procedure 
        for item in itemSet:
            result_list=list(item)
            intersect=self.__vertical_intersect(Vertical_rep_frequent,result_list) # 
            support=float(len(intersect)/transactions.trans_num())
            if support>=minSup:
                freqItemSet.add(item)
                Itemsets[tuple(item)] = support
        return freqItemSet
    
    def apriori(self, minFrequency,verbose=False):
        """The apriori algorithm optimized by the idea of vertical Representation"""

        transactions=self.__data
        Vertical_rep_frequent=transactions.get_freq_Vertical_Rep(minFrequency) # To store the vertical representation of frequent items 
        ItemSet1=transactions.get_items()

        Itemsets = defaultdict(int) # It makes a dictionary that never raises key error. Instead, it returns a default value

        ItemsetsL1 = self.__FindEligimateItemSet(ItemSet1, transactions, minFrequency, Itemsets,Vertical_rep_frequent)
        SetLevel_K = ItemsetsL1
        k = 2
        while(SetLevel_K):
            candidateSet=set([i.union(j) for i in SetLevel_K for j in SetLevel_K if len(i.union(j)) == k])
            candidateSet = self.__Pruning(candidateSet, SetLevel_K, k-1)
            SetLevel_K = self.__FindEligimateItemSet(candidateSet, transactions, minFrequency, Itemsets,Vertical_rep_frequent)
            k += 1
        if verbose==True:
            for i in Itemsets:
                print(str(list(sorted(i)))+' '+"("+str(Itemsets[i])+')')
            print(len(Itemsets), 'itemsets are found using Apriori Algorithm for min-Threshold=', minFrequency)


        return Itemsets

    # Apriori Graph Algorithm
    # Graph_based_apriori (An optimized Version, enhanced by vertical representation)

    def __AprioriGraph(self,result_list,minSup,vertex1,webaddr,answer,data,supports,Vertical_rep_frequent):
        count=0
        for vertex2 in webaddr[vertex1]:
            if (webaddr[vertex1][vertex2]>minSup) and (vertex2 not in result_list):
                result_list.append(vertex2)
                count+=1
                self.__AprioriGraph(result_list,minSup,vertex2,webaddr,answer,data,supports,Vertical_rep_frequent)
        if result_list not in answer:
            intersect=self.__vertical_intersect(Vertical_rep_frequent,result_list)

            found_conf=len(intersect)
            if found_conf>=minSup:
                answer.append(frozenset(result_list))
                supports[tuple(result_list)]=found_conf/data.trans_num()
        result_list.pop()
        return True
    
    def apriori_graph(self,minFrequency,verbose=False ):
        '''
        This is the graph-based apriori algorithm proposed by Pritish Yuvraj and Suneetha K. R. in 
        Modified Apriori Graph Algorithm for Frequent Pattern Mining.
        '''
        data=self.__data
        L1=data.get_freq_items(minFrequency)
        Vertical_rep_frequent=data.get_freq_Vertical_Rep(minFrequency) # To store the vertical representation of frequent items 
        minSup=(minFrequency-.00000001)*data.trans_num()
        webaddr={}
        supports={}
        trans_n=data.trans_num()
        for item1 in L1:
            webaddr[item1]={item2:0 for item2 in L1 } # Creating Webaddr
        for tid in range(data.trans_num()):
            t=data.get_transaction(tid) 
            for ct1,ct2 in combinations(t, 2):
                try:
                    webaddr[ct1][ct2]+=1
                except:

                    continue
        answer=[] # Global Variables 
        result_list=[]
        for vertex1 in L1:
            result_list=[]
            result_list.append(vertex1)
            self.__AprioriGraph(result_list,minSup,vertex1,webaddr,answer,data,supports,Vertical_rep_frequent)
        if verbose==True:
            for i in supports:
                print(str(list(sorted(i)))+' '+"("+str(supports[i])+')')
            print(len(supports), 'itemsets are found using Apriori Graph Algorithm for min-Threshold=', minFrequency)
        return supports
    
    # ECLAT Algorithm
    def __vr_intersect(self,vr,projected_vr,left,right):
        left=frozenset(left)
        right=frozenset(right)
        intersect=projected_vr.get(left,set())
        intersect=intersect.intersection(vr.get(right,set()))
        return intersect

    def eclat(self,minFrequency,verbose=False):
        """Eclat Algorithm- Recursive implementation"""
        data=self.__data
        vp=data.get_freq_Vertical_Rep(minFrequency) 
        total_trans = data.trans_num() 
        Itemsets={}
        items=data.get_freq_items(minFrequency)
        explored=items.copy()
        for idx in range(len(items)):
            item=items[idx]
            ExploredNew=explored.copy()
            ExploredNew=ExploredNew[idx:]
            supp=(len(vp[frozenset([item])])/data.trans_num())
            if supp>=minFrequency:
                Itemsets[tuple([item])]=supp
                projected_vr={}
                projected_vr[frozenset([item])]=vp[frozenset([item])]
                self.__depthFirstSearch(item, minFrequency, total_trans,vp,Itemsets,ExploredNew,projected_vr)
                del (projected_vr)
        if verbose==True:
            for i in Itemsets:
                print(str(list(sorted(i)))+' '+"("+str(Itemsets[i])+')')
            print(len(Itemsets), 'itemsets are found using ECLAT for min-Threshold=', minFrequency)

        return Itemsets
    def __depthFirstSearch(self,item,minFrequency, total_trans,vp,Itemsets,explored,projected_vr):
        exploredLocal=explored.copy()
        if type(item)!=list:
            item=[item]
        while (len(exploredLocal)>0):
            item2=exploredLocal.pop()
            if item2 not in item:
                item2=[item2]
                intersect=self.__vr_intersect(vp,projected_vr,item,item2)
                supp=len(intersect)/total_trans
                if(supp >= minFrequency):
                    itemsorted=sorted(item+item2)
                    if tuple(itemsorted) not in Itemsets:
                        Itemsets[tuple(itemsorted)]=supp
                        projected_vr[frozenset(item+item2)]=intersect
                        self.__depthFirstSearch(itemsorted,minFrequency, total_trans,vp,Itemsets,exploredLocal,projected_vr)
        return None
            
            