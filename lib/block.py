import numpy as np
import cv2
from .image import Image 

class Block:
    _x: int
    _y: int
    _w: int
    _h: int
    _c: int # channel
    block:np.ndarray
    data = {}


    def __init__(self, block) -> None:

        '''h, w, c = im.shape '''
        self.block =  np.array(block)
        (self._h, self._w)  = self.block.shape
        
    @property
    def x(self)-> int:
        return self._x
    
    @x.setter
    def x(self,x):
        self._x = x

    @property
    def y(self)-> int:      
        return self._y
    
    @y.setter
    def y(self,y):
        self._y = y

    @property
    def h(self)-> int:
        return self._h
    
    @property
    def w(self)-> int:
        return self._w
    
    @w.setter
    def w(self, w) ->None:
        self._w = w

    @h.setter
    def h(self, h) ->None:
        self._h = h

    def block_info(self) ->tuple:
        '''取得block 的資訊 '''
        self.data['X'] = self._x
        self.data['Y'] = self._y
        self.data['W'] = self._w
        self.data['H'] = self._h
        self.data['data'] = self.block
        self.data['block_avg'] = int (self.block.mean())
        self.data['block_min'] = self.block.min()
        return self.data
    
    def avg(self) -> int:
        '''算出block 中 pixels 平均值 '''
        return int(self.block.mean())

    def min(self) -> int:
        '''算出block 中 pixels 最小值'''
        return int(self.block.min())
    
    
    def to_np(self):
        ''' 轉成將block 轉為 np array'''
        return np.array(self.block)
    
    def to_image(self,filename=None,is_save=False)->Image:
        if is_save and filename is not None:
            if filename is None:
                raise FileNotFoundError("file name null")
            cv2.imwrite(filename,self.block)
       
        return np.array(self.block)
    
    
    def clone(self) -> float:
        ''' 複製一份區塊 '''
        return Block(self.block.copy(), self.x, self.y)
    
    def show_image(self):
        img = self.block.astype(np.uint8)
        cv2.imshow('block',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
  
    def is_the_same_pixel(self):
        '''判斷區塊內的像素值是否都一樣為平均值'''        
        avg = self.avg()
        x = self.to_np()
        mask = (x == avg)
        if mask.all() == True:
            return True
        else:
            return False 
        
    def __str__(self):
        return f"x:{self._x}, y:{self._y}, block:{self.block} "         

    



    



    

    
    
   


