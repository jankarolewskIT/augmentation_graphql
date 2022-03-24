import pathlib
import random
import os
import string

import requests

import query_loader

"""
Module runs get_test_image function for test purposes 
"""


def get_test_image(url: str) -> None:
    """
    Loads random images to BASE_DIR/test_images directory
    :param url:
    :return: None
    """
    formats = ["jpeg", "png", "bmp"]
    size = 10
    response = requests.get(url)
    file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))
    test_image_dir = os.path.join(pathlib.Path(__file__).parent.parent.parent, "test_images")
    if not os.path.isdir(test_image_dir):
        os.makedirs(test_image_dir)
    with open(os.path.join(test_image_dir, f"{file_name}.{random.choice(formats)}"),
              "wb") as file:
        file.write(response.content)


def main(url: str, amount: int = 10):
    for _ in range(amount):
        get_test_image(url)
    query_loader.create_query_data()


if __name__ == '__main__':
    URL = f"https://picsum.photos/{random.randint(50, 500)}/{random.randint(50, 500)}"
    main(URL)
