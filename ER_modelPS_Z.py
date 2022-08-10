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



n = 10
Tmax = 5000
niter = 1

random.seed(1234567890)


Datas = []

################ Lists
Liste_p = [0.15, 0.5, 0.8, 1]# [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,  0.8, 0.9, 1]
Liste_al = [0.001,  0.8, 1,  1.5]#[0.001]#,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
Liste_qb = [0.7, 0.8, 0.9, 1]

Qa = 1 #probability to change from 0-->1
P1 = int(n/2)
nums = P1 * [1] + (n - P1) * [0]    
#random.shuffle(nums)
########################### ZEALOTS #######################################

########## 
Nzel_0=1 #Number of Zealots with opinion 1
Nzel_1=1 #Number of Zealots with opinion 0

Threshold = 1#(n-Nzel_0)/n

############################### Opinion of the whole nodes ################
#### Here the normal nodes have the value 2 just to create the object #####

#############################################################################
iz = 0


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
                


                connected_net = False
                while not connected_net:
                    G = nx.erdos_renyi_graph(n,p)
                    connected_net = nx.is_connected(G)
                    
                Opinion = np.array(nums)
                Nombre_ones = [np.sum(Opinion)/float(n)]
                #print(Opinion)
####################################################################################################
                while iz<1:
                    idz0, idz1  = [], []
                    j, jj = 0, 0

                    ID=random.sample(G.nodes(), 4*Nzel_0)
                    for z in ID:
                        if Opinion[z]==0 and j<Nzel_0:
                            idz0.append(z)
                            j=j+1
                        if Opinion[z]==1 and jj<Nzel_1:
                            idz1.append(z)
                            jj=jj+1
                    iz = iz + 1
                    print(idz1)
                    print(idz0)
###################################################################################################

                qualities=[Qa, Qb]
                ####################################################
                cond = 0
                t = 0
                
                while (cond == 0):
                    random_node = random.sample(list(G.nodes()), 1)

                    ### We need to verify if the selected agent is not a zealot
                    for random_node in idz0 or idz1:
                        pass
                    else:
                        # List of neighbors
                        neighbors = list(G.neighbors(random_node))
                        # Neighbor Opinions
                        vocal_neighbors = []
                        for neigh in neighbors:
                            if random.random() < qualities[ Opinion[neigh] ]:
                                vocal_neighbors.append(Opinion[neigh])

                        if len(vocal_neighbors)>0:
                            # Fraction of opinions one in the list
                            Nombre_ones_select = np.sum(vocal_neighbors) / float(len(vocal_neighbors))

                            #print(Nombre_ones_select)   
                            if Nombre_ones_select > 0.5:
                                prob = (abs(Nombre_ones_select - 0.5) ** al) * (2 ** (al - 1)) + 0.5
                                    
                            else:
                                prob = -(abs(Nombre_ones_select - 0.5) ** al) * (2 ** (al - 1)) + 0.5
                                
                            Rand_num = random.random()
                            if Rand_num < prob:
                                Opinion[random_node] = 1

                            else:
                                Opinion[random_node] = 0
                                    

                    Nombre_ones_tmp = np.sum(Opinion)/float(n-Nzel_0)
                    Nombre_ones.append(Nombre_ones_tmp)
                    #print(Nombre_ones_tmp)
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
