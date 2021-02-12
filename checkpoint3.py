import cv2 
import numpy as np

class Node:
    def __init__(self, state, parent, action,pathList):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathList = pathList


#drawLines function
def drawLines(c):
    for i in c:
        c.remove(i)
        for j in c:
            cv2.line(img,(i[0],i[1]),(j[0],j[1]),(255,0,0),4)

def detectCountourType(types):
    rz =[]
    gz = []
    dp = []
    rc = []
    for c in types:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        color = img[cy,cx]
        if color[2]>=100 and color[1]<90 and color[0]<90:
            rz.append([cx,cy])
            rc.append(c)
        elif color[1]>=100 and color[2]<90 and color[0]<90:
            gz.append([cx,cy])
        else:
            dp.append([cx,cy])
        
    return gz,rz,dp,rc


def findPaths(gz,sp): 
    paths = []
    gz = gz + sp
    a = gz.copy()
    for g in gz:
        a.remove(g)
        for i in a:
            paths.append([g,i])
    return paths

def eliminatePathThroughRedZone(path,r):
    rp = []
    for p in path:
        points_on_line = np.linspace(p[0], p[1], 20)
        for a in points_on_line:
            if cv2.pointPolygonTest(r,tuple(a),False) == -1.0:
                continue
            elif cv2.pointPolygonTest(r,tuple(a),False) == 1.0:
                rp.append(p)
                break
    for p in rp:
        path.remove(p)

    return path

#input image
img = cv2.imread('checkpoint3.jpg')

#performing operation to get binary image and contours
height, width, channel = img.shape
img = cv2.resize(img , (0,0), fx=0.5 , fy=0.5)
imgc = img
imgc = cv2.cvtColor(imgc , cv2.COLOR_BGR2GRAY)
imgc = cv2.GaussianBlur(imgc, (5, 5), 0)
retVal ,imgc = cv2.threshold(imgc ,125,255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(imgc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
imgc_inverse = cv2.bitwise_not(imgc)
#black image
bg = np.zeros([img.shape[0],img.shape[1],img.shape[2]],dtype=np.uint8)
countour_og = []
for c in contours:
    if cv2.contourArea(c)>40:
        countour_og.append(c)


#get lists of everything
greenZone,redZone,startPoint,redCountours = detectCountourType(countour_og)

#find all possible paths
paths = findPaths(greenZone,startPoint)

#remove paths through red zones
for r in redCountours:
    paths = eliminatePathThroughRedZone(paths,r)

#calculate distance for each path
distance = []
for p in paths:
    d = int(((p[0][0]-p[1][0])**2 + (p[0][1]-p[1][1])**2)**0.5)
    distance.append(int(d))


#shortest path
exp_nodes = []
all_nodes = []
path_node =  []
target = startPoint[1]
node = Node(parent = None,state=startPoint[0],action = 0,pathList=[startPoint[0]])
exp_nodes.append(node)
all_nodes.append(node)
while True:
    if len(exp_nodes) == 0:
        print('no solution')
        break

    n = exp_nodes.pop(0)
    all_nodes.append(n)

    if n.state == target:
        print('found shortest path')
        n.pathList += [target]
        final_path =  n.pathList[1:]
        break

    for p in paths:
        if p[0] == n.state:
            exp_nodes.append(Node(parent = n.state,state =p[1],action =n.action +int(((p[0][0]-p[1][0])**2 + (p[0][1]-p[1][1])**2)**0.5),pathList = n.pathList+[n.state]))
        
        elif p[1] == n.state:
            exp_nodes.append(Node(parent = n.state,state =p[0],action =n.action +int(((p[0][0]-p[1][0])**2 + (p[0][1]-p[1][1])**2)**0.5),pathList = n.pathList+[n.state]))
     

for i in range(len(final_path)-1):
    cv2.line(img,tuple(final_path[i]), tuple(final_path[i+1]),(255,0,0),4)     


#displaying image
cv2.imshow("Image", img)
cv2.imwrite('output3.png',img)
cv2.waitKey(0)
cv2.destroyAllWindows()