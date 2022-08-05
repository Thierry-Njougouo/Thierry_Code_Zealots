import random
import numpy as np

random.seed(1234567890)
########################### ZEALOTS #######################################
n=10 #number of total nodes
########## 
Nzel_0=2 #Number of Zealots with opinion 1
Nzel_1=2 #Number of Zealots with opinion 0

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


##################### Here we build the opinions of the total nodes (Normal agents + Zealots)
Opinion=[]
PNa = int(PNa_1) * [1] + (Na - int(PNa_1)) * [0]
random.shuffle(PNa)
ii=0
for j in Opinion_z:
	if j==False:
		a=PNa[ii]
		Opinion.append(a)
		ii=ii+1
	else:
		Opinion.append(True)



print(Na)
print(Zealot)
print(Opinion_z)          
print(Opinion) 
print(len(Opinion)) 
print(np.sum(Opinion)-Nzel_0-Nzel_1)         