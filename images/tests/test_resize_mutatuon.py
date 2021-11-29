from django.conf import settings
import io
import json
from PIL import Image
import base64
from graphene_django.utils.testing import GraphQLTestCase


class ImageResizeTestCase(GraphQLTestCase):
    def test_mutation_connection(self):
        response = self.query(
            """
            mutation {
             resizeImage(
              input: {base64: "test", width: 200, height:200}
            )
              {
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

    def test_mutation_execution(self):

        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            initial_base64 = request.get("base64")
            new_width, new_height = 300, 350
            response = self.query(
                f"""
                mutation {{
                 resizeImage(
                  input: {{base64: "{initial_base64}", width: {new_width}, height:{new_height}}}
                )
                  {{
                        image {{
                      id
                      base64
                      path
                    }}  
                    }} 
                }}
                """
            )

            resized_image_base64 = json.loads(response.content.decode('utf-8'))['data']['resizeImage']['image']['base64']
            resized_image_bytes = base64.b64decode(resized_image_base64)
            resized_image = Image.open(io.BytesIO(resized_image_bytes))

            resized_width, resized_height = resized_image.size

            self.assertEqual(new_height, resized_height)
            self.assertEqual(new_width, resized_width)


