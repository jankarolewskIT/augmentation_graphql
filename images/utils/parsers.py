import base64


def pars_data(image, buffer, format_='JPEG'):
    """
    Prepare objects to be save to DB
    :param image: Pillow Image obj
    :param buffer: Bytes obj
    :param format_: JPG/BMP/PNG
    :return: tuple(bytes, str)
    """
    image.save(buffer, format_)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    img_data = base64.b64decode(img_str)
    return img_data, img_str
