import base64
import io
import json

from PIL import Image
from django.conf import settings
from graphene_django.utils.testing import GraphQLTestCase


class ImageNegativeTestCase(GraphQLTestCase):
    def test_negative_connection(self):
        """Test connection. Is status code: 200 OK"""
        response = self.query(
            """
            mutation {
                negateImage (input: {base64: ""}){
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

    def test_negation(self):
        """Work in progress"""
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for query in data:
            initial_base64_str = query.get("base64")
            initial_base64_data = base64.b64decode(initial_base64_str)
            initial_image = Image.open(io.BytesIO(initial_base64_data))

            response = self.query(
                f"""
                mutation {{
                    negateImage (input: {{base64: "{initial_base64_str}"}}){{
                        image{{
                            id
                            base64
                            path
                        }}
                    }}
                }}
                """
            )

            negative_base64_str = json.loads(response.content.decode('utf-8'))['data']['negateImage']['image']['base64']
            negative_base64_data = base64.b64decode(negative_base64_str)
            negative_image = Image.open(io.BytesIO(negative_base64_data))
            mode_negative = negative_image.mode
