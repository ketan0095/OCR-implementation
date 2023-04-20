from flask import Flask,jsonify,request
from flask_cors  import CORS
from methods.ocr_functions import paddle_ocr,pytesseract_ocr,easy_ocr
from methods.img_processing import PIL_TO_BASE64
import time,os,cv2
from PIL import Image


app = Flask(__name__)
CORS(app)
INSTALLATION_PATH =os.getcwd()
DUMP_PATH =os.path.join(INSTALLATION_PATH,"temp")


@app.route('/')
def hello_world():
    return jsonify({
        "status":200,
        "msg":"success"
    })

@app.route("/ocr/generate-result", methods=['POST'])
def generate_result():

    # download file
    data = request.files.getlist('files')

    if len(data) == 0:
        # no files uploaded
        return jsonify({
            "status": 501,
            "data": "Image not found !"
        })
    
    file_to_be_processed =[]

    for ind, i in enumerate(data):


        download_path = os.path.join(DUMP_PATH, i.filename)
        i.save(download_path)

        # convert img to be jpg

        file_to_be_processed.append((download_path,i.filename))

    total_payload ={"data":[]}

    for file_ in file_to_be_processed:
        # run paddle ocr
        img_read =cv2.imread(file_[0])
        _,ocrdata,input_image =paddle_ocr(img_read)

        # output
        payload ={
            "Image_name":file_[1],
            "Image_size":os.path.getsize(file_[0]),
            "OCR_data":ocrdata,
            "Image_dimensions":img_read.shape,
            # "Image_buffer":PIL_TO_BASE64(Image.open(file_[0]))
            "Image_buffer":PIL_TO_BASE64(input_image,cv2_flag=True),
            "Image_model":"PaddleOCR"
        }

        total_payload["data"].append(payload)

        # run pytesseract
        img_read_1 =cv2.imread(file_[0])
        ocrdata,input_image =pytesseract_ocr(img_read_1)

        # output
        payload ={
            "Image_name":file_[1],
            "Image_size":os.path.getsize(file_[0]),
            "OCR_data":ocrdata,
            "Image_dimensions":img_read.shape,
            # "Image_buffer":PIL_TO_BASE64(Image.open(file_[0]))
            "Image_buffer":PIL_TO_BASE64(input_image,cv2_flag=True),
            "Image_model":"PyTesseract"
        }

        total_payload["data"].append(payload)

        # run easy OCR
        ocrdata,input_image =easy_ocr(file_[0])

        # output
        payload ={
            "Image_name":file_[1],
            "Image_size":os.path.getsize(file_[0]),
            "OCR_data":ocrdata,
            "Image_dimensions":img_read.shape,
            # "Image_buffer":PIL_TO_BASE64(Image.open(file_[0]))
            "Image_buffer":PIL_TO_BASE64(input_image,cv2_flag=True),
            "Image_model":"EasyOCR"
        }

        total_payload["data"].append(payload)

    
    # print(len(total_payload["data"]))

    return jsonify({
        "status":200,
        "msg":"success",
        "result":total_payload
    })


if "__main__"==__name__:
    app.run(host="0.0.0.0",port=3636,debug=True)
