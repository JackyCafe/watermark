from msaLib import MsaImage
from block import Block
from misc import divide_block,get_th
import logging
import sys
import cv2

logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s [%(levelname)s] %(message)s",
    format="",
    handlers=[
        logging.FileHandler(".orginal1.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

location_block = 3
# watre_mark_image = MsaImage('ncut.png') # 浮水印 image
cover_image = MsaImage('1.png')  #原圖
#從1.png 中取63 X 63 的區塊
cover_image.rows=63
cover_image.cols=63
locates = cover_image.get_block_locate()
#從cover_image取第 index 個block 存成 watermark_area，要做浮水印的區域

watermark_area = cover_image.get_block(location_block) 
watermark_area.block_to_image('block3.png')

watermark_area_blocks = divide_block(watermark_area,3 ,3) # 將 watermark_area 浮水印區域 切成3X3 的 block 依序存成 blocks的list
average_pixel = watermark_area.avg()    #計算watermark_area 的平均pixels   
th_pixel = get_th(average_pixel,w=30)    #依定義從新計算閥值   
#1. 讀取ncut.png，並做二值化，定義此圖為water_mark
watermark = MsaImage('2.png') 
im_bw = watermark.to_binary_image()
#將ncut 以th = 128 分為0/1 二值化
bw_blocks = Block(im_bw)
bw_blocks.x = 0
bw_blocks.y = 0

# 將浮水印的圖以3X3 切成block 後丟入list-->watermark_blocks
watermark_blocks = divide_block(bw_blocks, 3, 3 ) 
new_block_list = []
x = 0
y = 0

for index,b in  enumerate(watermark_blocks):

    b = watermark_area_blocks[index] #取出第i個 浮水印區域
    wm = watermark_blocks[index]   #取出第i個 浮水印
    bx = b.block  
    wx = wm.block
    cols = b.block.shape[0]
    rows = b.block.shape[1]
    new_block_array = [[0 for x in range(cols)] for y in range(rows)]
    for i in range(cols):
        for j in range(rows):
            if b.avg()<th_pixel:
                new_block_array[i][j] = bx[i][j]+wx[i][j]*20
            else:
                new_block_array[i][j] = bx[i][j]-wx[i][j]*20    
    new_block = Block(new_block_array)
    new_block.x = x
    new_block.y = y
    x = x + 1  
    if x ==21:
        y = y + 1
        x = 0 
    
    new_block_list.append(new_block)
    # print(len(new_block_list))
    

#重建影像

b1_img = MsaImage.reconstruct_image(new_block_list,cols=63,rows=63,w=3,h=3)
recontruct_image=cover_image.set_block(location_block,b1_img)

cv2.imshow('img',recontruct_image)
cv2.imwrite('recontruct_image.png',recontruct_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

