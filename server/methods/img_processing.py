import base64
from io import BytesIO
from PIL import Image
import cv2


def PIL_TO_BASE64(image,cv2_flag =False):

    """
    image : PIL Image
    """

    if cv2_flag:
        retval, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode("utf-8")
    
    else:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

# print(PIL_TO_BASE64(Image.open(r"C:\ketan personal\OCR Demo\ocr_app\public\test.jpg"))[:10])