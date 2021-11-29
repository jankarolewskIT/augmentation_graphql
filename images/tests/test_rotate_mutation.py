import json

from django.conf import settings
from graphene_django.utils.testing import GraphQLTestCase


class ImageRotateTestCase(GraphQLTestCase):
    def test_rotate_connection(self):
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

    def test_rotation(self):
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            initial_base64 = request.get("base64")
            angle = 360
            response = self.query(
                f"""
                mutation {{
                    rotateImage (input: {{base64: "{initial_base64}", angle:{angle}}}){{
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

            self.assertAlmostEqual(initial_base64, rotate_image_base64)
            # full_rotation_angle = 360 - angle
            # full_rotation_response = self.query(
            #     f"""
            #     mutation {{
            #         rotateImage (input: {{base64: "{rotate_image_base64}", angle:{full_rotation_angle}}}){{
            #             image {{
            #                 id
            #                 base64
            #                 path
            #             }}
            #         }}
            #     }}
            #     """
            # )
            #
            # back_rotated_base64 = json.loads(full_rotation_response.content.decode('utf-8'))['data']['rotateImage']['image']['base64']
            #
            # self.assertEqual(initial_base64, back_rotated_base64)

