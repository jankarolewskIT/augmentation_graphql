import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from PIL import Image as PillowImage
import base64
from io import BytesIO
import json
from django.core.files.base import ContentFile

from .models import Image


class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        fields = ['id', 'base64', 'path']


class ImageNode(DjangoObjectType):
    class Meta:
        model = Image
        filter_fields = {
            'path': ['exact', 'icontains']
        }

        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    all_images = graphene.List(ImageType)
    image = relay.Node.Field(ImageNode)

    def resolve_all_images(self, info, **kwargs):
        return Image.objects.all()


class ImageResizeMutation(relay.ClientIDMutation):
    class Input:
        base64 = graphene.String(required=True)
        width = graphene.Int(required=True)
        height = graphene.Int(required=True)
        path = graphene.String()

    image = graphene.Field(ImageType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        initial_base64 = kwargs.get('base64')
        bytes_img = initial_base64.encode('utf-8')
        original_data = base64.b64decode(bytes_img)
        original_buffer = BytesIO(original_data)
        pillow_img = PillowImage.open(original_buffer)
        resized_img = pillow_img.resize((kwargs.get('width'), kwargs.get('height')))

        new_buffer = BytesIO()

        resized_img.convert('RGB').save(new_buffer, format="JPEG")
        resized_img_str = base64.b64encode(new_buffer.getvalue()).decode('utf-8')
        resized_img_data = base64.b64decode(resized_img_str)

        obj = Image.objects.create(
            base64=resized_img_str,
            path=ContentFile(resized_img_data, name="resized_img.jpeg")
        )
        return ImageResizeMutation(obj)


class Mutation:
    resize_image = ImageResizeMutation.Field()
