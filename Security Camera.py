import cv2
import numpy as np
import skimage.measure

addcolor = (0, 0, 50)
imagesize = (480,640,3)
blocksize = 1
blurshape = (int(imagesize[0]/blocksize),int(imagesize[1]/blocksize),imagesize[2])
nframes = 10
colorsensitivity = 50
areaSensitivity = 10000

cap = cv2.VideoCapture(0)
H = np.array(np.zeros(shape=((1,)+blurshape)), dtype=np.uint8)

while True:
    ret, frame = cap.read()
    blur = skimage.measure.block_reduce(frame, block_size=(blocksize,blocksize,1), func=np.mean).astype(np.uint8)
    #we sample the image in blocks of blocksize pixels | we use the average of each block for our new pixel values
    #the reason we downsample is to reduce computation time and storage
    
    H = np.insert(H,0, blur,axis=0)                 #insert new frame at beginning of list
    if H.shape[0] > nframes:                        #checks if the amount of stored frames is larger than 10
        H = np.delete(arr=H, obj=nframes, axis=0)   #deletes oldest frame

    avg = skimage.measure.block_reduce(H, block_size=(nframes,1,1,1), func=np.mean)[0]
    #finds the average pixel color of last nframes frames
    
    dif = abs(avg-blur).astype(np.uint8)    #finds the difference in color from the average and the current frame
    motion = dif > colorsensitivity
    #creats a true or false array, if a pixel is true then it has changed more than the sensitivity
    
    motionmap = motion * blur

    #detects whether there is motion
    if np.sum(motion) > areaSensitivity:
        print('Motion!!!!')
    else: print('-----------------')

    addcolor = motion * (255 - blur)
    
        
    cv2.imshow('WebCam',frame)
#    cv2.imshow('Motion', motionmap.astype(np.uint8))
#    cv2.imshow('Colored', dif)
    cv2.imshow('a', blur + addcolor.astype(np.uint8))
    #cv2.resizeWindow('Colored',imagesize[1],imagesize[0])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
