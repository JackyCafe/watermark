import cv2
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",help="choice a file",default="pics/squirrel.jpg")
    parser.add_argument("-o",help="choice a file",default="pics/squirrel.jpg")
    parser.add_argument("-s",help="set up size",type=int)

    args = parser.parse_args()
    input = args.f
    size = args.s
    output = args.o
    img = cv2.imread(input)
    img = cv2.resize(img,(size,size))
    cv2.imwrite(output,img)


if __name__=='__main__':
    main()
