import base64
import functools
from io import BytesIO

from PIL import Image as PillowImage


def prepare_image(func):
    """
    Mutation decorator design to prepare images to be cropped, negated, compressed, resized or rotated
    """

    @functools.wraps(func)
    def wrapper(instance, root, info, **kwargs):
        initial_base64 = kwargs.get('base64')
        bytes_img = initial_base64.encode('utf-8')
        original_data = base64.b64decode(bytes_img)
        original_buffer = BytesIO(original_data)
        if PillowImage.open(original_buffer).mode not in ['RGB', 'L']:
            kwargs['pillow_img'] = PillowImage.open(original_buffer).convert("RGB")
        else:
            kwargs['pillow_img'] = PillowImage.open(original_buffer)
        return func(instance, root, info, **kwargs)

    return wrapper
