import mazing_gym as gym
import numpy as np
from PIL import Image
import cv2
import random


class Root:
    def __init__(self, limit, blocks):
        self.count = 0
        self.last = ""
        self.banned = []


        self.map = blocks
        self.free = gym.free(self.map)
        self.limit = limit
        self.leafes = []
        self.max = 0
        for i in self.free:
            self.leafes.append(Leaf(self, i))
            self.limit -= 1
        while(self.limit > 0):
            self.get_max().expand()
            print(self.limit)
            print(self.max)
        m = self
        while(m.leafes != []):
            for i in m.leafes:
                if(i.max == self.max):
                    m = i

        print(m.max)
        
        env = np.zeros((20, 18, 3), dtype=np.uint8)
        for i in self.map:
            env[i[0]][i[1]] = d[BLOCK_N]
        for i in m.map:
            if i not in self.map:
                env[i[0]][i[1]] = d[4]
        for i in gym.pathfind(m.map):
            env[i[1]][i[0]] = d[PATH_N]
        env[0][9] = d[END_N]
        env[0][10] = d[END_N]
        env[19][9] = d[END_N]
        env[19][10] = d[END_N]
        img = Image.fromarray(env, 'RGB')
        img = img.resize((600, 600))
        cv2.waitKey(0)
        cv2.imshow("image", np.array(img)) 
        cv2.waitKey(20000)
        cv2.destroyAllWindows()

            
    def get_max(self):
        maximum = 0
        self.max_arr = []
        for i in self.leafes:
            if(i.max > maximum and i not in self.banned):
                maximum = i.max
        
        for i in self.leafes:
            if(i.max == maximum):
                self.max_arr.append(i)
        mm = random.choice(self.max_arr)
        if(self.last != mm):
            self.last = mm
        else:
            self.count += 1
        if(self.count == 10):
            self.banned.append(self.last)
            self.last = ""
            self.count = 0
        if len(self.banned) > 6:
            self.banned = []

        return mm

        
class Leaf(Root):
    def __init__(self, root, cord):
        self.count = 0
        self.last = ""
        self.banned = []


        self.root = root
        self.map = self.root.map.copy()
        self.map.append(cord)
        self.map.append([cord[0], cord[1]+1])
        self.map.append([cord[0]+1, cord[1]])
        self.map.append([cord[0]+1, cord[1]+1])                    
        self.free = gym.free(self.map)
        self.max = gym.path_len(self.map)
        self.push()
        self.leafes = []
        

    def push(self):
        m = self
        while(hasattr(m, 'root')):
            if m.root.max < m.max:
                m.root.max = m.max
            m = m.root
            
    def expand(self):
        if(self.max == 0):
            return 
        if self.leafes == []:
            for i in self.free:
                self.leafes.append(Leaf(self, i))
                m = self
                while(not hasattr(m, 'limit')):
                    m = m.root
                m.limit -= 1
        else:
            self.get_max().expand()
if __name__ == "__main__":            
    d = {1: (255, 0, 0),
         2: (0, 255, 0),
         3: (0, 0, 255),
         4: (55, 55, 55)}
    PATH_N = 1
    END_N = 2
    BLOCK_N = 3
    test = gym.create_map(20)
    root = Root(1000, test)
