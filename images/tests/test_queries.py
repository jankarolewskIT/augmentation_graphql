import json

from graphene_django.utils.testing import GraphQLTestCase

from ..models import Image


class ImageTestCase(GraphQLTestCase):
    """
    Tests for GraphQL Queries
    """
    def test_all_images_query(self):
        """
        Test if response show no errors and if __len__ of
        response.content (all Images) is the same as __len__ of Queryset form DB
        """
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

        content_len = len(json.loads(response.content.decode('utf-8'))['data']['allImages'])
        db_len = len(Image.objects.all())

        self.assertEqual(content_len, db_len)
        self.assertResponseNoErrors(response)

    def test_image_query(self):
        """
        Test if Image can be found and retrieve by it's ID
        """
        obj = Image.objects.create(base64="", path="")


        response = self.query(
            f"""
            query {{
                image (id: {obj.id}){{
                    id
                    base64
                    path
                }}
            }}
            """
        )
        response_base64 = json.loads(response.content.decode('utf-8'))['data']['image']['base64']
        self.assertEqual(obj.base64, response_base64)
        self.assertEqual(response.status_code, 200)
