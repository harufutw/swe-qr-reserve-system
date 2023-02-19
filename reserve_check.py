import cv2
import collections
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def last_row(sheet):
    str_list = list(filter(None,sheet.col_values(1)))
    return len(str_list)

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
        try :
            retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(trimming)
        except :
            continue
        if retval:
            if decoded_info[0] != '':
                decode_list.append(decoded_info[0])
        frame = cv2.addWeighted(edit_frame, 0.4, frame, 0.6, 0)
        frame = cv2.resize(frame, (width_sv, height_sv))
        cv2.imshow('camera',frame)
        k = cv2.waitKey(10)
        if len([i for i, j in collections.Counter(decode_list).items() if j > threshold]) > 0:
            return [i for i, j in collections.Counter(decode_list).items() if j > threshold][0]
            cap.release()
            cv2.destroyAllWindows()
        if k == 27 :
            [collections.Counter(decode_list).items()]
            cap.release()
            cv2.destroyAllWindows()
            return 'quited'

scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
credentials = ServiceAccountCredentials.from_json_keyfile_name("reserve-check-377912-a65e15cfd7e3.json", scopes=scope)
#OAuth2の資格情報を使用してGoogle APIにログイン。
gc = gspread.authorize(credentials)
#スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = '1EP7F5XcxgbUtNuMD9eCJhPwXDpIAPrryxvJJUg0NqDU'
# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)
worksheet = workbook.worksheet('フォームの回答 1')


while True:
    result = read_qrcode(0)
    if result == 'quited':
        break
    ticket_id = ''
    flag = False
    for i in range(last_row(worksheet)):
        row = worksheet.row_values(i+1)
        j = 0
        while j < len(row):
            if row[j] == result:
                flag = True
                email = row[1]
                num_ticket = row[2]
                console = '{0}枚　{1}さん'.format(num_ticket,email)
                break
            j += 1
        if flag:
            break
    
    if not flag:
        console = '404 error'
    print(console)