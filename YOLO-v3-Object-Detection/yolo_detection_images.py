import numpy as np
import cv2

#img_path = 'images/person.jpg'
def detectObjects(img_path):
    confidenceThreshold = 0.5
    NMSThreshold = 0.3

    modelConfiguration = 'cfg/yolov3.cfg'
    modelWeights = 'yolov3.weights'

    labelsPath = 'coco.names'
    labels = open(labelsPath).read().strip().split('\n')

    np.random.seed(10)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

    #image = cv2.imread(img_path) #이미지 파일들을 flag 값에 따라 읽어드림
    encoded = np.fromstring(img_path,dtype=np.uint8)
    # byte mode로 읽었는데 data 정보를 uint8 형태로 반환하는 것을 알 수 있음 1D-array
    # 그러고나서 encoded를 이미지 바이트 스트림을 3D-array로 만들어주어야 한다.
    image = cv2.imdecode(encoded,cv2.IMREAD_COLOR)
    print(type(image))
    (H, W) = image.shape[:2]

    #return numpy.ndarray
    #Determine output layer names 파일 경로를 읽는 return은 이미지 객체 행렬
    layerName = net.getLayerNames()
    layerName = [layerName[i - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB = True, crop = False)
    net.setInput(blob)
    layersOutputs = net.forward(layerName)

    boxes = []
    confidences = []
    classIDs = []

    for output in layersOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidenceThreshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY,  width, height) = box.astype('int')
                x = int(centerX - (width/2))
                y = int(centerY - (height/2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    #Apply Non Maxima Suppression
    detectionNMS = cv2.dnn.NMSBoxes(boxes, confidences, confidenceThreshold, NMSThreshold)

    outputs = {}
    final = []
    string_final =""

    #json으로 보여줌
    if len(detectionNMS) > 0:
        outputs['detections'] = {}
        outputs['detections']['labels']=[]
        for i in detectionNMS.flatten():
            detection= {} # 여기에 json 정보 들어감 dictionary 형태
            detection['Label']= labels[classIDs[i]] # key = value 값
            final.append(labels[classIDs[i]]) # 리스트에 인식한 라벨 모두 넣기
           # detection['confidence'] = confidences[i]
            #detection['X'] = boxes[i][0]
            #detection['Y'] = boxes[i][1]
            #detection['Width'] = boxes[i][2]
            #detection['Height'] = boxes[i][3]
            print(type(labels[classIDs[i]]))
            outputs['detections']['labels'].append(detection)
    else:
        outputs['detections'] = 'No object detected'

    string_final =" ".join(final)
    return string_final

#print(labels[classIDs[i]])
#print(confidences[i])
#print(boxes[i][0])
#print(boxes[i][1])
#print(boxes[i][2])
#print(boxes[i][3])
