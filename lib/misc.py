from lib.block import Block
from lib.point import Point
import numpy as np

def divide_block(b:Block, cols:int, rows:int )->list:
    '''丟一個wafer_marker 的 Block 進來，拆成nXn 的大小'''
    blocks = []
    location = [] 
    w = b.w
    h = b.h
    new_block = np.array(np.zeros((cols, rows), dtype= np.int32))
    for i in range(0, w,  cols):    
        for j in range(0, h, rows):
                p = Point(i, j)
                location.append(p)    
    for n,l in enumerate(location):
       x = l.x
       y = l.y
       new_block = Block(b.block[x:x+cols,y:y+rows])  
       new_block.x = x
       new_block.y = y
       blocks.append(new_block)   

    return blocks


def get_th(avg_pixel,w=30):
     ''' 自定義的閥值，如果64X64 block 的平均值(avg_pixel)<=128
         閥值 = avg_pixel+w(default=30) 否則 
         閥值 = avg_pixel-w(default=30)
     '''
     return avg_pixel+30 if avg_pixel <=128 else avg_pixel-30  
