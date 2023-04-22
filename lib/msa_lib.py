'''Msa Lib
   含很多function 
'''

import cv2
import numpy as np
from lib.point import Point
from lib.image import Image
from lib.block import Block
from .util import logging as log


class MsaImage:
    '''Msa lib '''
    W: int
    H: int    
    _cols: int
    _rows: int
    locates = []
    blocks = [tuple]

    def __init__(self, filename: str) -> None:
        self.im = cv2.imread(filename,0) 
        h, w = self.im.shape
        self.W = w
        self.H = h


    @property
    def cols(self) ->int:
        '''block 的 cols'''
        return self._cols

    @cols.setter    
    def cols(self, x: int):
        self._cols = x

    @property
    def rows(self) ->int :
        '''block 的 rows'''
        return self._rows        


    @rows.setter
    def rows(self, y: int):
        self._rows = y    

    def set_block(self,index:int,block:Block)->Image:
        '''將block 塞回第index 位置'''
        s =64
        ratio = self.W // s
        x = index//ratio #更改 512/128 = 4
        y = index%ratio #更改
        print(f'(x,y)=({x},{y})')
        for i in range(self.cols):
            for j in range(self.rows):
                self.im[(x)*s+i][(y)*s+j]= block[i][j]

        return self.im             

    def get_block_by_xy(self, x:int, y:int)->Block:
        '''給定x,y 座標，傳回一個block(cols,rows)'''
        block = np.array(np.zeros((self.cols,self.rows,3),dtype= np.int32))
        # block = [[0 for x in range(self.cols)] for y in range(self.rows)]

        for i in range(x,x+self.cols):
            for j in range(y, y+self.rows):
                block[i-x][j-y] = self.im[i][j]
        new_block = Block(block)
        new_block.x = self.cols
        new_block.y = self.rows   
        print(new_block)     
        return new_block 
        
    def get_block_locate(self) -> list:
        ''' 將一張影像依 NXN 大小分割成小的block,
            並把位置記錄在p的物件，位置從(0,0),(0,N),(0,2N)...開始
            存放在locates 的list 
            return locates list
        '''

        self.locates = []
        # print(f'w:{self.W}')
        # print(f'cols:{self.cols}') 
        for i in range(0, self.W, self.cols):
            for j in range(0, self.H, self.rows):
                p = Point(i, j)
                self.locates.append(p)
        return self.locates
   

    def get_block(self,index)->Block:
        ''' 傳回第 index 個 block 的物件'''
        x: int = self.locates[index].x
        y: int = self.locates[index].y
        
        #block 為一個 cols X rows 大小的block
        block = np.array(np.zeros((self.cols,self.rows),dtype= np.int32))

        # block = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for i in range(x, x + self.cols):
            for j in range(y, y + self.rows):
                block[i - x][j - y] = self.im[i][j] 
                # if (x+self.cols<self.W)>0 and (y+self.rows<self.H):
                #   block[i - x][j - y] = self.im[i][j]  
                # else:
                #     continue    
        block_obj = Block(block)  
        block_obj.x= x
        block_obj.y= y     
        return block_obj        
    

    def to_binary_image(self) ->Image:
        '''將圖轉為binary'''
        img_bw = cv2.threshold(self.im,127,255, cv2.THRESH_BINARY)[1]
        threshold =128
        img_bw[img_bw>threshold]=1
        return img_bw

    @classmethod
    def reconstruct_image(cls, blocks, cols=64, rows=64,w=2,h=2 ):
        '''將block list 的圖堆回原圖'''
        dst:Image
        dst = np.zeros([rows,cols],dtype=np.int32)
        r = rows//w
       
        for i,block in enumerate(blocks) :
            for x in range(w):
                for y in range(h):
                    dst[(i//r)*2+x][(i%r)*2+y] = block.block[x][y]
        cv2.imwrite('watermarker.png',dst)
        return dst

    def resize(self, w, h):
        '''resize 圖檔'''
        return cv2.resize(self.im, w, h)
    
    def show_image(self)->None:
        img = self.im
        cv2.imshow('block',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        



