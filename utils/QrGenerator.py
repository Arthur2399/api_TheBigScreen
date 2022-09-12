import qrcode
import os
from djcines.settings import DIR
def Generator(text,path,fil):
    qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 10,
            border = 4
            )
    qr.add_data(text)
    dir=DIR+"media"
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(dir+path):
        os.makedirs(dir+path)
    #qr.png(dir+"")
    imagen = qr.make_image()
    imagen.save(dir+path+fil)
    
