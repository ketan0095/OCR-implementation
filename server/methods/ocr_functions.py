
from paddleocr import PaddleOCR, draw_ocr
import cv2
import pytesseract
from pytesseract import Output
import os
import easyocr

# for Linux : sudo apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
reader = easyocr.Reader(['en']) 

def paddle_ocr(input, ocr=None):
    """
    input : cv2 image object 
    ocr : paddle ocr object 
    return : [string,center-y,rect-cord-of-string,center-x]
    """
    if ocr == None:
        ocr = PaddleOCR(use_angle_cls=True, show_log=False, lang='en')
    result = ocr.ocr(input)
    text_list = []

    json_result ={"data":[]}
    for i in result:

        data_to_append={
            "value":i[1][0],
            "accuracy":i[1][1],
            "dimensions":"{}".format(i[0])
        }
        json_result["data"].append(data_to_append)
        try:
            text_list.append([i[1][0], 
                              i[0][0][1] + (i[0][2][1] - i[0][0][1])/2,
                              i[0][0] + i[0][2], 
                              i[0][0][0] + (i[0][2][0] - i[0][0][0])/2])
            
            input = cv2.rectangle(
                input,
                (int(i[0][0][0]),int(i[0][0][1])),
                (int(i[0][2][0]),int(i[0][2][1])),
                # (0,0),
                # (100,100),
                (0, 0, 255),
                1
            )
        except Exception as e:
            print("result :", i,e)
    
    cv2.imwrite("tets.jpg",input)
    return text_list,json_result,input

def check_string(text:str):
    if text.isalnum() or text.isnumeric():
        return True
    return False

def pytesseract_ocr(input,accuracy_flag =20):

    d = pytesseract.image_to_data(input, config="--psm 6", output_type=Output.DICT)
    n_boxes = len(d['level'])

    json_result ={"data":[]}
    
    for i in range(n_boxes):
        
        if(d['text'][i] != "") and check_string(d['text'][i]) and d['conf'][i]>=accuracy_flag:
            data_to_append={
            "value":d['text'][i],
            "accuracy":d['conf'][i],
            "dimensions":"{}".format([d['left'][i], d['top'][i], d['width'][i], d['height'][i]])
        }
            json_result["data"].append(data_to_append)
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(input, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return json_result,input

def easy_ocr(img_path:str):

    result = reader.readtext(img_path)
    img_read =cv2.imread(img_path)
    json_result ={"data":[]}

    for data in result:
        data_to_append={
            "value":data[1],
            "accuracy":data[2],
            "dimensions":"{}".format(data[0])
        }

        json_result["data"].append(data_to_append)
        cv2.rectangle(img_read, (int(data[0][0][0]), int(data[0][0][1])), (int(data[0][2][0]), int(data[0][2][1])), (0, 255, 0), 2)

    return json_result,img_read



if "__main__"==__name__:

    img =cv2.imread(r"C:\ketan personal\OCR Demo\server\temp\WhatsApp Image 2023-03-16 at 1.31.18 PM.jpeg")
    # print(pytesseract_ocr())

    