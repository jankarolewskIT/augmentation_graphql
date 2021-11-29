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

        self.assertResponseNoErrors(response)

    def test_mutation_execution(self):
        # make sure to use every image in json file
        # Think about another testing approach
        width, height = 300, 350
        response = self.query(
            f"""
            mutation {{
             resizeImage(
              input: {{base64: "test", width: {width}, height:{height}}}
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