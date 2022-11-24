from importlib.resources import path
import pyqrcode

path = "./qr_codes/"

def CreateQRCode(content: str):
    forward_slash = "/"

    qr_code = pyqrcode.create(content)
    
    new_content = content.replace("/", "").replace(":", "")

    print(new_content)
           
    qr_png = path + new_content + ".png"
    qr_code.png(qr_png, scale=8)

CreateQRCode("https://youtube.com")
