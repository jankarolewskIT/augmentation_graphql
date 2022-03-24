import base64
import json
import os
import pathlib


def create_query_data() -> None:
    """
    Function called at the beginning of container is run, to populate json_data file.
    :return: None
    """
    directory = os.fsencode(f"{pathlib.Path(__file__).parent.parent.parent}/test_images/")
    request_list = []
    for image in os.listdir(directory):
        image = image.decode('utf-8')
        with open(f"{pathlib.Path(__file__).parent.parent.parent}/test_images/{image}", "rb") as file:
            base64_str = base64.b64encode(file.read()).decode('utf-8')

            request = {
                "base64": base64_str,
            }

            request_list.append(request)
        with open(f"{pathlib.Path(__file__).parent.parent.parent}/json_data.json", "w") as file:
            json.dump(request_list, file, indent=4)
