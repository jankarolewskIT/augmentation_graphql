import graphene

from images.schema import Query as ImageQuery, Mutation as ImageMutation


class Query(ImageQuery, graphene.ObjectType):
    pass


class Mutation(ImageMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
