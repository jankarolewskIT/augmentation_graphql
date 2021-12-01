import base64
import io
import json

from PIL import Image
from django.conf import settings
from graphene_django.utils.testing import GraphQLTestCase


class ImageCropMutation(GraphQLTestCase):
    def test_connection(self):
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)

        base64_ = data[0].get('base64')
        left = 100
        top = 100
        right = 125
        bottom = 125

        response = self.query(
            f"""
            mutation {{
                cropImage (input: {{base64: "{base64_}", left: {left}, top: {top}, right:{right}, bottom:{bottom}}}){{
                    image{{
                        id
                        base64
                        path
                    }}
                }}
            }}
            """
        )

        self.assertEqual(response.status_code, 200)

    def test_raise_crop_error(self):
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)

        base64_ = data[0].get('base64')
        left = 100
        top = 100
        right = 90
        bottom = 90

        response = self.query(
            f"""
            mutation {{
                cropImage (input: {{base64: "{base64_}", left: {left}, top: {top}, right:{right}, bottom:{bottom}}}){{
                    image{{
                        id
                        base64
                        path
                    }}
                }}
            }}
            """
        )

        self.assertResponseHasErrors(response)

    def test_cropped(self):
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)

        left = 100
        top = 100
        right = 125
        bottom = 125

        for query in data:
            initial_base64 = query.get("base64")
            cropped_response = self.query(
                f"""
                mutation {{
                  cropImage(input: {{base64: "{initial_base64}", left: {left}, top: {top}, right:{right}, bottom:{bottom}}}){{
                    image{{
                        id
                        base64
                        path
                    }}
                  }}  
                }}
                """
            )

            cropped_base64_str = json.loads(cropped_response.content.decode('utf-8'))['data']['cropImage']['image'][
                'base64']
            cropped_data = base64.b64decode(cropped_base64_str)
            cropped_img = Image.open(io.BytesIO(cropped_data))
            cropped_width, cropped_height = cropped_img.size

            self.assertEqual(cropped_height, bottom - top)
            self.assertEqual(cropped_width, right - left)
