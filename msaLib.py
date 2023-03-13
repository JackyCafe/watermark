import cv2
from point import Point
from block import Block
from image import Image
import numpy as np
import logging

class MsaImage:
    '''
        W: 圖檔寬
        H: 圖檔高
        cols: block 寬
        rows: block 高
    '''
    W: int
    H: int    
    _cols: int
    _rows: int
    locates = []
    blocks = [tuple]


    def __init__(self, filename:str) -> None:
        '''
            filename: 檔名
            x: block 寬
            y: block 高 
        '''
        self.image = cv2.imread(filename=filename)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        self.W = self.image.shape[0]
        self.H = self.image.shape[1]

    @property
    def cols(self) ->int:
        return self._cols

    @cols.setter    
    def cols(self, x: int):
        self._cols = x

    @property
    def rows(self) ->int :
        return self._rows        


    @rows.setter
    def rows(self, y: int):
        self._rows = y    

    def get_block(self,index)->Block:
        ''' 傳回第 index 個 block 的物件'''
        x: int = self.locates[index].x
        y: int = self.locates[index].y
        
        #block 為一個 cols X rows 大小的block
        block = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for i in range(x, x + self.cols):
            for j in range(y, y + self.rows):
                 
                if (x+self.cols<self.W)>0 and (y+self.rows<self.H):
                    block[i - x][j - y] = self.image[i][j]
                else:
                    continue    
        block_obj = Block(block)  
        block_obj.x= x
        block_obj.y= y       
        return block_obj        


    def set_block(self,index:int,block:Block)->Image:
        '''將block 塞回第index 位置'''
        x = index//20
        y = index%20
        print(f'(x,y)=({x},{y})')
        for i in range(self.cols):
            for j in range(self.rows):
                self.image[(x)*63+i][(y)*63+j]= block[j][i]

        return self.image        
   
    def get_block_locate(self) -> list:
        ''' 將一張影像依 NXN 大小分割成小的block,
            並把位置記錄在p的物件，位置從(0,0),(0,N),(0,2N)...開始
            存放在locates 的list 
            return locates list
        '''

        self.locates = []
        for i in range(0, self.W, self.cols):
            for j in range(0, self.H, self.rows):
                p = Point(i, j)
                self.locates.append(p)
        return self.locates
    

    def to_binary_image(self) ->Image:
        '''將圖轉為binary'''
        img_bw = cv2.threshold(self.image,127,255,cv2.THRESH_BINARY)[1]
        threshold =127
        img_bw[img_bw>threshold]=1
        return img_bw
    
    
    
    @classmethod
    def reconstruct_image(cls,blocks,cols=63,rows =63, w=3,h=3)->Image:
        dst: Image
        dst = np.zeros([rows,cols],dtype=int)
        for block in blocks:
            x = block.x
            y = block.y
            for i in range(w):
                for j in range(h):
                    dst[x*w+i][y*h+j] = block.block[i][j]    
        cv2.imwrite('watermarker.png',dst)        
        return dst                    
    
    