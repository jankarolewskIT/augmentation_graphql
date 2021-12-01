import base64
import io
import json

from PIL import Image
from django.conf import settings
from graphene_django.utils.testing import GraphQLTestCase


class ImageRotateTestCase(GraphQLTestCase):
    """
    Tests for rotateImage mutation
    """

    def test_rotate_connection(self):
        """Test connection. Is status code: 200 OK"""
        response = self.query(
            """
            mutation {
                rotateImage (input: {base64: "", angle:180}){
                    image {
                        id
                        base64
                        path
                    }
                }
            }
            """
        )

        self.assertEqual(response.status_code, 200)

    def test_rotation_90(self):
        """
        Test if Image's width and height are switched after 90' degrees rotation
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for query in data:
            initial_base64_str = query.get("base64")
            initial_base64 = base64.b64decode(query.get("base64"))
            initial_image = Image.open(io.BytesIO(initial_base64))

            initial_width, initial_height = initial_image.size

            angle = 90
            response = self.query(
                f"""
                mutation {{
                    rotateImage (input: {{base64: "{initial_base64_str}", angle:{angle}}}){{
                        image {{
                            id
                            base64
                            path
                        }}
                    }}
                }}
                """

            )

            rotate_image_base64 = json.loads(response.content.decode('utf-8'))['data']['rotateImage']['image']['base64']
            rotated_img_data = base64.b64decode(rotate_image_base64)
            rotated_image = Image.open(io.BytesIO(rotated_img_data))

            rotated_width, rotated_height = rotated_image.size

            self.assertAlmostEqual(initial_width, rotated_height)
            self.assertAlmostEqual(initial_height, rotated_width)
