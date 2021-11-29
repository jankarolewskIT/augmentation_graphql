import base64


def pars_data(image, buffer, format_='JPEG'):
    image.save(buffer, format_)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    img_data = base64.b64decode(img_str)
    return img_data, img_str
