
# from ..lib.msa_lib import MsaImage
from lib.msa_lib import MsaImage
from lib.util import logging as log
from lib.misc import divide_block,get_th
from lib.block import Block
import cv2
import numpy as np
import os
import math

def sigmoid(x:int)->float:
    return 1/(1+np.exp(-x))

def tanh(x:int)->float:
   return (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))

def leaky_relu(x):
  if x>0 :
    return x
  else :
    return 0.01*x
  

def mleaky_relu(x):
  if x>0 :
    return x
  else :
    return -0.001*(x)


def main():
    locate = 23
    cover_im =  MsaImage('pics/1.png') #原飛機圖
    cover_im.rows = 64
    cover_im.cols = 64
    locates = cover_im.get_block_locate()
    watermark_area = cover_im.get_block(locate) #從cover_image取第 index 個block 存成 watermark_area，要做浮水印的區域
    # 將 watermark_area 浮水印區域 切成2X2 的 block 依序存成 blocks的list
    watermark_area_blocks = divide_block(watermark_area,2 ,2)
    average_pixel = watermark_area.avg()    #計算watermark_area 的平均pixels   
    th_pixel = get_th(average_pixel,w=30)    #依定義從新計算閥值   
    # b1_img = MsaImage.reconstruct_image(watermark_area_blocks,w=2,h=2)
 
    watermark = MsaImage('pics/333.png') #松鼠圖
    im_bw = watermark.to_binary_image()
    bw_blocks = Block(im_bw)
    bw_blocks.x = 0
    bw_blocks.y = 0
    
    # 將浮水印的圖以3X3 切成block 後丟入list-->watermark_blocks
    watermark_blocks = divide_block(bw_blocks, 2, 2 ) 
    new_block_list = []
    x = 0
    y = 0

    for index,b in  enumerate(watermark_blocks):
        b = watermark_area_blocks[index] #取出第i個 浮水印區域
        wm = watermark_blocks[index]   #取出第i個 浮水印
        bx = b.block  
        wx = wm.block
        cols = b.block.shape[1]
        rows = b.block.shape[0]
        new_block_array = [[0 for x in range(cols)] for y in range(rows)]
        for i in range(cols):
            for j in range(rows):
                # if watermark_area.avg()==0:
                #     new_block_array[i][j] = bx[i][j]+abs(wx[i][j]-1)*255
                if b.avg()<th_pixel:
                    # new_block_array[i][j] = bx[i][j]+wx[i][j]*60
                    new_block_array[i][j] = bx[i][j]+(tanh((th_pixel - b.avg())) + 2)*wx[i][j]*30
                else:
                    # new_block_array[i][j] = bx[i][j]-wx[i][j]*60 
                    new_block_array[i][j] = bx[i][j]-(tanh((th_pixel - b.avg())) + 2)*wx[i][j]*30  
        new_block = Block(new_block_array)
        new_block_list.append(new_block)
    b1_img = MsaImage.reconstruct_image(new_block_list,w=2,h=2)
    recontruct_image=cover_im.set_block(locate,b1_img)

    cv2.imshow('img',recontruct_image)
    cv2.imwrite(f'watermark_{locate}.jpg',recontruct_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    



if __name__=='__main__':
    main()