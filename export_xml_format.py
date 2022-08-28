import numpy as np
import cv2 as cv
import PIL
import xml.etree.ElementTree as ET

vd = cv.VideoCapture('test_video.mp4')
# Passing the path of the xml document to enable the parsing process
tree = ET.parse('annotations.xml')
 
# getting the parent tag of the xml document
root = tree.getroot()

#create a dic where we will put for each frame the coreespond labels (points positions)
dic = {}
for neighbor in root.iter('polygon'):
    frame = neighbor.attrib.get('frame')
    points = neighbor.attrib.get('points')
    array_splited_points = np.array([[[0,0]]]) 
    splited_points = points.split(';')
    for pt in splited_points:
        y = pt.split(',')
        x = np.array([[[round(float(y[0])),round(float(y[1]))]]])
        array_splited_points = np.insert(array_splited_points,-1,x,axis=0)
    dic[f'frame {frame}'] = array_splited_points = array_splited_points[:-1]

cpt = 1
while(vd.isOpened()):
    ret, frame = vd.read()
    if ret == True:
        img_mod = cv.polylines(frame, [dic[f'frame {cpt}']], True, (255,120,255),3)       
        cv.imshow('video', img_mod) 
        cpt = cpt+1
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    # Break the loop
    else:
        break 
      
cv.waitKey(0)
cv.destroyAllWindows()