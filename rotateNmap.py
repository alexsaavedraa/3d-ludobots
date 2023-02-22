import numpy as np
import random as random
from scipy.spatial.transform import Rotation as R


import numpy as np

seed = 0
#rand.random(seed)


###A top level Body should look like this:
#    |
#it will have a major axis and 1-2 minor axis
    #one minor axis with symetry
#   -|-

#       >|<

#   /|/
def find_largest_integer(nested_list):
    max_val = float('-inf')
    for item in nested_list:
        if isinstance(item, int):
            max_val = max(max_val, item)
        elif isinstance(item, list):
            max_val = max(max_val, find_largest_integer(item))
    return max_val



def rotateCoords(coords, angles):

    
    # define the vector you want to rotate
    v = np.array(coords).reshape(3, 1)

    r1 = R.from_euler('yx', [angles[1], angles[0]], degrees=True).as_matrix()
    r2 = R.from_euler('z', angles[2], degrees=True).as_matrix()
    r_combined = r2 @ r1

    # apply the rotation
    v_rotated = r_combined @ v
    v_rotated = np.round(v_rotated, decimals = 4)
    # interpret the result
    #print(v_rotated)
    v_final = np.array(v_rotated).reshape(1, 3)[0]
    #this process creates negative 0s

    #print(v_final)
    return v_final


x = 1
y =0
z = 0
Xangle = 0
Yangle = 180
Zangle = 0

rotateCoords([x,y,z],[Xangle,Yangle,Zangle])

def count_integers(lst):
    total = 0
    for i, item in enumerate(lst):
        if isinstance(item, list):
            total += 0.5
            total += count_integers(item)
        elif isinstance(item, int) and i in range(2, 7) and item > 0:
            total += 1
    return total

def botmap(ID, parId, symmetry, dorsal_p, lr_p, tb_p, xAx, yAx, zAx, depth):

    '''take in number of parts, bool sym, seed, left-right limb probability, tb limb probability'''
    random.seed(ID)
    currID = 0
    lmap  = [0]* 11
    successmap =  [0]*11
    lmap[0] = ID
    lmap[1] = parId


    successmap[2] = random.choices([1, 0], weights=[dorsal_p, 1-dorsal_p], k=1)[0]
    lmap[2] = sum(successmap) + lmap[0]  

    successmap[3] = random.choices([1, 0], weights=[lr_p, 1-dorsal_p], k=1)[0] 
    lmap[3] = (find_largest_integer(lmap)+1)*successmap[3]
    successmap[4] = random.choices([1, 0], weights=[lr_p, 1-dorsal_p], k=1)[0] 
    lmap[4] = (find_largest_integer(lmap)+1)*successmap[4]
    successmap[5] =  random.choices([1, 0], weights=[tb_p, 1-dorsal_p], k=1)[0]
    lmap[5] = (find_largest_integer(lmap)+1)*successmap[5]
    successmap[6] = random.choices([1, 0], weights=[tb_p, 1-dorsal_p], k=1)[0]    
    lmap[6] = (find_largest_integer(lmap)+1)*successmap[6]
    lmap[7] = xAx
    lmap[8] = yAx
    lmap[9] = zAx
    lmap[10] = depth

   
    


    if symmetry:
        pass
        #lmap[6] = lmap[5] + 1
        #lmap[4] = lmap[3] + 1
    count =  sum(lmap[2:7])        
    return lmap, count





def build(num_parts, count,listp, listposn, head):
        heads = head
        
        working, countn = botmap(find_largest_integer(listp)+1,head, True, .8, .6, .4, 0, 1, 0,0)
        if listposn == 3:
            working[7:10] = rotateCoords(working[7:10], [0,0,90]).tolist()  
        if listposn == 4:
            working[7:10] = rotateCoords(working[7:10], [0,0,-90]).tolist() 
        if listposn == 5:
            print("rotating listposn ", 5)
            working[7:10] = rotateCoords(working[7:10], [90,0,0]).tolist() 
        if listposn == 6:
            working[7:10] = rotateCoords(working[7:10], [-90,0,0]).tolist()     


        if not(isinstance(listp[listposn], list)) and listp[listposn] > 0:
            
            listp[listposn] = [find_largest_integer(listp)+1, working]
            heads +=1
            print("increasing heads because instance of 1")
        if (countn+count >= num_parts):
             #print("returning 0")
             return 0
        else:
             for i, item in enumerate(listp[2:7]):
                  if not(isinstance(item, list)) and count_integers(listp) <= num_parts:
                       #print("building anoter list at posn ", i+2)
                       
                       if item > 0:
                        heads+=1
                        build(num_parts, countn+count,  listp, i +2, find_largest_integer(listp))


        print("the count is ", count_integers(listp))
        return listp
             

def gen_dorsal(num_parts, curr):
    num = random.randint(1,num_parts)
    dorsals = [0]* (num+1)
    id = curr + num

    dorsals[0] = num;
    for i in range(1,num+1):
        if id + i <= num_parts:
            dorsals[i] = id + i

    return(dorsals)

def get_body(num_parts):


    #start, count = botmap(0, 0, True, .8, .6, .4, 0, 1,0,0)
    print(gen_dorsal(num_parts,0))

    return gen_dorsal(num_parts,0)

get_body(5)