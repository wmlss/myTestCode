import sys
import cv2
import os
import dlib
import glob
import math
import numpy as np
from skimage import io

# predictor_path = sys.argv[1]
# faces_folder_path = sys.argv[2]
predictor_path = 'shape_predictor_68_face_landmarks.dat'
faces_folder_path = 'faces'
pointsArray = []

def shape_to_np(shape):
    coords = np.zeros((68, 2), dtype = int)

    for i in range(0, 68):
        coords[i] = (int(shape.part(i).x), int(shape.part(i).y))
    return coords
#1.使用dlib自带的frontal_face_detector作为我们的人脸提取器
detector = dlib.get_frontal_face_detector()
#2.使用官方提供的模型构建特征提取器
predictor = dlib.shape_predictor(predictor_path)

for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):

        print("Processing file: {}".format(f))
        img = io.imread(f)#读取图片
        #人脸提取
        dets = detector(img, 1)
        arr = []
        for k, d in enumerate(dets):
            shape = predictor(img, d) #提取脸部特征
            shape_np = shape_to_np(shape) #使用predictor进行人脸关键点识别
            pointsArray.append(shape_np)  #添加到记录数组
            # np.savetxt(f + '.txt', shape_np, fmt = '%i')

# Read all jpg images in folder.
def readImages(path) :

    #Create array of array of images.
    imagesArray = [];

    #List all files in the directory and read points from text files one by one
    for filePath in os.listdir(path):
        if filePath.endswith(".jpg"):
            # Read image found. 形式为BGR
            img = cv2.imread(os.path.join(path,filePath));

            # Convert to floating point
            img = np.float32(img)/255.0;

            # Add to array of images
            imagesArray.append(img);

    return imagesArray;

# Compute similarity transform given two sets of two points.
# OpenCV requires 3 pairs of corresponding points.
# We are faking the third one.

def similarityTransform(inPoints, outPoints) :
    s60 = math.sin(60*math.pi/180);
    c60 = math.cos(60*math.pi/180);

    inPts = np.copy(inPoints).tolist();
    outPts = np.copy(outPoints).tolist();

    xin = c60*(inPts[0][0] - inPts[1][0]) - s60*(inPts[0][1] - inPts[1][1]) + inPts[1][0];
    yin = s60*(inPts[0][0] - inPts[1][0]) + c60*(inPts[0][1] - inPts[1][1]) + inPts[1][1];

    inPts.append([np.int(xin), np.int(yin)]);

    xout = c60*(outPts[0][0] - outPts[1][0]) - s60*(outPts[0][1] - outPts[1][1]) + outPts[1][0];
    yout = s60*(outPts[0][0] - outPts[1][0]) + c60*(outPts[0][1] - outPts[1][1]) + outPts[1][1];

    outPts.append([np.int(xout), np.int(yout)]);

    tform = cv2.estimateRigidTransform(np.array([inPts]), np.array([outPts]), False);

    return tform;


# Check if a point is inside a rectangle 检查点是否在矩形内
def rectContains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

# Calculate delanauy triangle  计算三角剖分
def calculateDelaunayTriangles(rect, points):
    # Create subdiv
    subdiv = cv2.Subdiv2D(rect);

    # Insert points into subdiv
    for p in points:
        subdiv.insert((p[0], p[1]));


    # List of triangles. Each triangle is a list of 3 points ( 6 numbers )
    triangleList = subdiv.getTriangleList();

    # Find the indices of triangles in the points array

    delaunayTri = []

    for t in triangleList:
        pt = []
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rectContains(rect, pt1) and rectContains(rect, pt2) and rectContains(rect, pt3):
            ind = []
            for j in range(0, 3):
                for k in range(0, len(points)):
                    if(abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)
            if len(ind) == 3:
                delaunayTri.append((ind[0], ind[1], ind[2]))

    return delaunayTri


def constrainPoint(p, w, h) :
    p =  ( min( max( p[0], 0 ) , w - 1 ) , min( max( p[1], 0 ) , h - 1 ) )
    return p;

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
#将使用srcTri和dstTri计算的仿射变换应用到src并输出大小的图像。
def applyAffineTransform(src, srcTri, dstTri, size) :

    # Given a pair of triangles, find the affine transform.
    #给定一对三角形，找到仿射变换。
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )

    # Apply the Affine Transform just found to the src image
    #将刚刚找到的仿射变换应用于src图像
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
# 经线和alpha将三角形区域从img1和img2混合到img
def warpTriangle(img1, img2, t1, t2) :

    # Find bounding rectangle for each triangle
    # 为每个三角形查找边界矩形
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    # 偏移点位于各个矩形的左上角
    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    #通过填充三角形获取面罩
    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    # 将warpImage应用于小矩形修补程序
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)

    img2Rect = img2Rect * mask

    # Copy triangular region of the rectangular patch to the output image
    # 将矩形色块的三角形区域复制到输出图像
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )

    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect



if __name__ == '__main__' :

    path = 'faces/'

    # Dimensions of output image 输出图像的尺寸
    w = 600;
    h = 600;

    # Read points for all images
    allPoints = pointsArray;

    # Read all images
    images = readImages(path);

    # Eye corners 眼角
    eyecornerDst = [ (np.int(0.3 * w ), np.int(h / 3)), (np.int(0.7 * w ), np.int(h / 3)) ];

    imagesNorm = [];
    pointsNorm = [];

    # Add boundary points for delaunay triangulation   三角剖分  为delaunay三角测量增加边界点
    boundaryPts = np.array([(0,0), (w/2,0), (w-1,0), (w-1,h/2), ( w-1, h-1 ), ( w/2, h-1 ), (0, h-1), (0,h/2) ]);

    # Initialize location of average points to 0s  初始化平均点的位置为0
    pointsAvg = np.array([(0,0)]* ( len(allPoints[0]) + len(boundaryPts) ), np.float32());

    n = len(allPoints[0]);

    numImages = len(images)

    # Warp images and trasnform landmarks to output coordinate system,
    # 将图像变形并将地标变换为输出坐标系，
    # and find average of transformed landmarks.
    # 并找出转化的地标的平均值。
    for i in range(0, numImages):

        points1 = allPoints[i];

        # Corners of the eye in input image  输入图像中眼睛的角落
        eyecornerSrc  = [ allPoints[i][36], allPoints[i][45] ];

        # Compute similarity transform 相似变换  输入眼角
        tform = similarityTransform(eyecornerSrc, eyecornerDst);

        # Apply similarity transformation  应用相似性转换
        img = cv2.warpAffine(images[i], tform, (w,h));

        # Apply similarity transform on points  对点应用相似变换
        points2 = np.reshape(np.array(points1), (68,1,2));

        points = cv2.transform(points2, tform);

        points = np.float32(np.reshape(points, (68, 2)));

        # Append boundary points. Will be used in Delaunay Triangulation
        # 追加边界点。 将用于Delaunay Triangulation
        points = np.append(points, boundaryPts, axis=0)

        # Calculate location of average landmark points.
        # 计算平均标志点的位置。
        pointsAvg = pointsAvg + points / numImages;

        pointsNorm.append(points);
        imagesNorm.append(img);



    # Delaunay triangulation  德劳内三角测量
    rect = (0, 0, w, h);
    dt = calculateDelaunayTriangles(rect, np.array(pointsAvg));

    # Output image
    output = np.zeros((h,w,3), np.float32());

    # Warp input images to average image landmarks  将输入图像转换为平均图像界标
    for i in range(0, len(imagesNorm)) :
        img = np.zeros((h,w,3), np.float32());
        # Transform triangles one by one  逐个转换三角形
        for j in range(0, len(dt)) :
            tin = [];
            tout = [];

            for k in range(0, 3) :
                pIn = pointsNorm[i][dt[j][k]];
                pIn = constrainPoint(pIn, w, h);

                pOut = pointsAvg[dt[j][k]];
                pOut = constrainPoint(pOut, w, h);

                tin.append(pIn);
                tout.append(pOut);


            warpTriangle(imagesNorm[i], img, tin, tout);


        # Add image intensities for averaging  添加图像强度以进行平均
        output = output + img;


    # Divide by numImages to get average 除以numImages得到平均值
    output = output / numImages;

    # Save result
    cv2.imwrite('myaverageface.png', (output * 255).astype('uint8'))
