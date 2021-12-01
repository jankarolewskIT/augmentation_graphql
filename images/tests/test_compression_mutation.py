from graphene_django.utils.testing import GraphQLTestCase


class ImageCompressionTestCase(GraphQLTestCase):
    """
    Test for compressImage mutation
    """
    def test_connection(self):
        """Test connection. Is status code: 200 OK"""
        response = self.query(
            f"""
            mutation {{
                compressImage (input: {{base64: "", quality: 1}}){{
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
