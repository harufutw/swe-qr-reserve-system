import cv2
import collections

def read_qrcode(threshold):
    cap = cv2.VideoCapture(1)
    qcd = cv2.QRCodeDetector()
    height_sv = 540
    width_sv = 960
    decode_list = []
    while True:
        ret, frame = cap.read()
        edit_frame = frame.copy()
        (height_pv, width_pv) = frame.shape[:2]
        cv2.rectangle(edit_frame, (0,0),(int(0.2*width_pv),height_pv),(0,0,0),thickness=-1)
        cv2.rectangle(edit_frame, (int((1-0.2)*width_pv),0),(width_pv,height_pv),(0,0,0),thickness=-1)
        cv2.rectangle(edit_frame, (0,0),(width_pv,int(0.1*height_pv)),(0,0,0),thickness=-1)
        cv2.rectangle(edit_frame, (0,int((1-0.1)*height_pv)),(width_pv,height_pv),(0,0,0),thickness=-1)
        trimming = frame[int(0.1*height_pv):int((1-0.1)*height_pv), int(0.2*width_pv):int((1-0.2)*width_pv)]
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(trimming)
        if retval:
            if decoded_info[0] != '':
                decode_list.append(decoded_info[0])
        frame = cv2.addWeighted(edit_frame, 0.4, frame, 0.6, 0)
        frame = cv2.resize(frame, (width_sv, height_sv))
        cv2.imshow('camera',frame)
        k = cv2.waitKey(10)
        if len([i for i, j in collections.Counter(decode_list).items() if j > threshold]) > 0:
            return [i for i, j in collections.Counter(decode_list).items() if j > threshold][0]
        if k == 27 :
            [collections.Counter(decode_list).items()]
            return 'quited'

result = read_qrcode(3)
print(result)