import json

from graphene_django.utils.testing import GraphQLTestCase


class ImageTestCase(GraphQLTestCase):
    def test_all_images_query(self):
        response = self.query(
            """
            query {
                allImages {
                    id
                    base64
                    path
                }
            }
            """
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

    def test_image_query(self):
        response = self.query(
            """
            query {
                image (id: 5){
                    id
                    base64
                    path
                }
            }
            """
        )

        self.assertEqual(response.status_code, 200)

