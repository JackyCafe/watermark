import numpy as np
from image import Image
import cv2

class Block:
    _x: int
    _y: int
    _w: int
    _h: int
    data = {}

    #初始化
    def __init__(self,block) -> None:
        self.block = np.array(block)
        self._w = self.block.shape[0]
        self._h = self.block.shape[1]
        
    
    @property
    def x(self)-> int:
        return self._x
    
    @property
    def y(self)-> int:      
        return self._y
    
    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y


    @property
    def w(self):
        return self._w
    
    @property
    def h(self):
        return self._h
    
    @w.setter
    def w(self, w):
        self._w = w

    @h.setter
    def h(self, h):
        self._h = h

    '''block 的資訊'''
    def get_block_info(self) -> tuple:
        self.data['X'] = self._x
        self.data['Y'] = self._y
        self.data['data'] = self.block
        self.data['block_avg'] = int(self.block.mean())
        self.data['block_min'] = self.block.min()
        return self.data

    def avg(self) -> int:
        '''算出block 中 pixels 平均值 '''
        return int(self.block.mean())

    def min(self) -> int:
        '''算出block 中 pixels 最小值'''
        return int(self.block.min())

    
    def clone(self) -> float:
        ''' 複製一份區塊 '''
        return Block(self.block.copy(), self.x, self.y)

    ''' 判斷區塊內的像素值是否都一樣'''
    def is_the_same_pixel(self):
        avg = self.avg()
        x = self.to_np()
        mask = (x == avg)
        if mask.all() == True:
            return True
        else:
            return False

    ''' 轉成np array'''
    def to_np(self):
        return np.array(self.block)
    
    def block_to_image(self,filename)->Image:
        cv2.imwrite(filename,self.block)
       
        return np.array(self.block)
    
    def show_image(self):
        cv2.imshow('block',self)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def __str__(self):
        return f"x:{self._x}, y:{self._y}, block:{self.block} "        