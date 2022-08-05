''' By Thierry N. and Giovanni. This code is used to generate consensus in BA model using qualities in the modify majority update rule.
We have considered One opinion and 500(niter) networks each formed by 100 nodes. '''

import networkx as nx
import matplotlib.pyplot as plt
import random
from random import sample
import numpy as np
import pylab
import csv
import pandas as pd
import statistics



n = 100
Tmax = 15000
niter = 100
Threshold = 1

random.seed(1234567890)


Datas = []

################ Lists
Liste_p = [0.15, 0.5, 0.8, 1]# [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,  0.8, 0.9, 1]
Liste_al = [0.001,  0.8, 1,  1.5]#[0.001]#,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
Liste_qb = [0.7, 0.8, 0.9, 1]

Qa = 1 #probability to change from 0-->1

########################### ZEALOTS #######################################

########## 
Nzel_0=5 #Number of Zealots with opinion 1
Nzel_1=5 #Number of Zealots with opinion 0

############################### Opinion of the whole nodes ################
#### Here the normal nodes have the value 2 just to create the object #####

Zealot = Nzel_1 * [1] + Nzel_0 * [0] + (n - Nzel_1 - Nzel_0) * [2]
random.shuffle(Zealot)

Opinion_z=[]
for i in Zealot:
    if i!=2:
        Opinion_z.append(True)
    else:
        Opinion_z.append(False)
                                                                            #
Opinion_z = np.array(Opinion_z)  
###### In the list Opinion_z the zealots are the nodes with opinion True ####

##### Here we build randomly the opinion of the nodes who are not zealots ###  
Na=n-Nzel_0-Nzel_1 #Na denotes the number of Normal agents
PNa_1=Na/2 #PNa_1 is the proportion of Normal agents with opinion 1
                                          #
##################### Here we build the opinions of the total nodes (Normal agents + Zealots)
Opinion_i=[]
PNa = int(PNa_1) * [1] + (Na - int(PNa_1)) * [0]
random.shuffle(PNa)
ii=0
for j in Opinion_z:
    if j==False:
        a=PNa[ii]
        Opinion_i.append(a)
        ii=ii+1
    else:
        Opinion_i.append(True)

#############################################################################



for Qb in Liste_qb:

    print(Qb)

    for al in Liste_al:

        for p in Liste_p:
            
            T = []
            
            j0 = 0
            j1 = 0
            jn = 0

            AA = Liste_p.index(p)
            

            for i in range(0,niter):
                random.seed(i + AA*niter)

                ########## Opinions
                random.shuffle(Opinion_i)


                connected_net = False
                while not connected_net:
                    G = nx.erdos_renyi_graph(n,p)
                    connected_net = nx.is_connected(G)
                    
                Opinion = np.array(Opinion_i)
                Nombre_ones = [(np.sum(Opinion)-Nzel_0)/float(n)]


                qualities=[Qa, Qb]
                ####################################################
                cond = 0
                t = 0
                
                while (cond == 0):
                    random_node = random.sample(list(G.nodes()), 1)

                    ### We need to verify if the selected agent is not a zealot
                    if Opinion[random_node]!=True:
                        # List of neighbors
                        neighbors = list(G.neighbors(random_node[0]))
                        # Neighbor Opinions
                        vocal_neighbors = []
                        for neigh in neighbors:
                            if Opinion[neigh]!=True:
                                if random.random() < qualities[ Opinion[neigh] ]:
                                    vocal_neighbors.append(Opinion[neigh])

                        if len(vocal_neighbors)>0:
                            # Fraction of opinions one in the list
                            Nombre_ones_select = np.sum(vocal_neighbors) / float(len(vocal_neighbors))

                           
                            if Nombre_ones_select > 0.5:
                                prob = (abs(Nombre_ones_select - 0.5) ** al) * (2 ** (al - 1)) + 0.5
                                
                            else:
                                prob = -(abs(Nombre_ones_select - 0.5) ** al) * (2 ** (al - 1)) + 0.5
                            
                            Rand_num = random.random()
                            if Rand_num < prob:
                                Opinion[random_node] = 1

                            else:
                                Opinion[random_node] = 0
                                

                    Nombre_ones_tmp = np.sum(Opinion)/float(n)
                    Nombre_ones.append(Nombre_ones_tmp)

                    #################################################################
                    if t < Tmax:
                        if (Nombre_ones_tmp >= Threshold):
                            T.append(t)
                            j1 = j1 + 1
                            cond = 1

                        elif (Nombre_ones_tmp <= 1 - Threshold):    
                            j0 = j0 + 1
                            T.append(t)
                            cond = 1

                        else:
                            t = t + 1
                    else:
                        cond = 1
                        jn = jn + 1
            

            Tm = np.mean(T)
            Tsd = np.std(T)
           



                        

######################################################################
##################### Save data ######################################
######################################################################

            filename = "Results/Time"+"_qb"+str(Qb)+"_al"+str(al)+"_m"+str(p)+".csv"
            file=open(filename,'w')
            write = csv.writer(file,delimiter ='\n') 
            write.writerow(T)
            file.close()


            

            datas = [Qa, Qb, al, p, j0, j1, jn, Tm, Tsd]
            new_lst = str(datas)[1:-1] 
            Datas.append(new_lst)
            filename_1 = "Results/data.csv"
            file_1=open(filename_1,'w')
            write = csv.writer(file_1, delimiter ='\n') 
            write.writerow(Datas)
            file_1.close()

           
######################################################################
##################### End Save data ##################################
######################################################################

print('Thanks, the simulation is finished')
