import base64
from io import BytesIO

import graphene
from PIL import ImageOps
from django.core.files.base import ContentFile
from graphene import relay
from graphene_django.types import DjangoObjectType

from .decorators.mutations_decorators import prepare_image
from .errors.mutation_errors import CropParametersError
from .errors.query_errors import IdRequiredError
from .models import Image
from .utils.parsers import pars_data


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
    image = graphene.Field(ImageType, id=graphene.Int(), required=True)

    def resolve_all_images(self, info, **kwargs):
        return Image.objects.all()

    def resolve_image(self, info, **kwargs):
        id_ = kwargs.get('id')
        if id_:
            return Image.objects.get(pk=id_)
        else:
            raise IdRequiredError('Argument id is required for this query')


class ImageResizeMutation(relay.ClientIDMutation):
    class Input:
        base64 = graphene.String(required=True)
        width = graphene.Int(required=True)
        height = graphene.Int(required=True)
        path = graphene.String()

    image = graphene.Field(ImageType)

    @classmethod
    @prepare_image
    def mutate_and_get_payload(cls, root, info, **kwargs):
        resized_img = kwargs['pillow_img'].resize((kwargs.get('width'), kwargs.get('height')))

        new_buffer = BytesIO()

        resize_image_data = pars_data(resized_img, new_buffer)

        obj = Image.objects.create(
            base64=resize_image_data[1],
            path=ContentFile(resize_image_data[0], name="resized_img.jpeg")
        )
        return ImageResizeMutation(obj)


class ImageCropMutation(relay.ClientIDMutation):
    class Input:
        base64 = graphene.String(required=True)
        left = graphene.Int(required=True)
        top = graphene.Int(required=True)
        right = graphene.Int(required=True)
        bottom = graphene.Int(required=True)

    image = graphene.Field(ImageType)

    @classmethod
    @prepare_image
    def mutate_and_get_payload(cls, root, info, **kwargs):
        left = kwargs.get('left')
        top = kwargs.get('top')
        right = kwargs.get('right')
        bottom = kwargs.get('bottom')

        crop_box = (left, top, right, bottom)

        if left > right or top > bottom:
            raise CropParametersError(
                """
                left can not be greater than right, 
                and top can not be greater than bottom
                """
            )

        new_buffer = BytesIO()
        crop_img = kwargs.get('pillow_img').crop(crop_box)

        cropped_image_data = pars_data(crop_img, new_buffer)

        obj = Image.objects.create(
            base64=cropped_image_data[1],
            path=ContentFile(cropped_image_data[0], name="crop_img.jpeg")
        )

        return ImageCropMutation(obj)


class ImageRotateMutation(relay.ClientIDMutation):
    class Input:
        base64 = graphene.String(required=True)
        angle = graphene.Int(required=True)

    image = graphene.Field(ImageType)

    @classmethod
    @prepare_image
    def mutate_and_get_payload(cls, root, info, **kwargs):
        angle = kwargs.get('angle')

        new_buffer = BytesIO()
        rotate_img = kwargs.get('pillow_img').rotate(angle, expand=True)
        rotated_data = pars_data(rotate_img, new_buffer)

        obj = Image.objects.create(
            base64=rotated_data[1],
            path=ContentFile(rotated_data[0], name="rotate_img.jpeg")
        )

        return ImageRotateMutation(obj)


class ImageNegativeMutation(relay.ClientIDMutation):
    class Input:
        base64 = graphene.String(required=True)

    image = graphene.Field(ImageType)

    @classmethod
    @prepare_image
    def mutate_and_get_payload(cls, root, info, **kwargs):
        new_buffer = BytesIO()

        negative_img = ImageOps.invert(kwargs.get('pillow_img'))
        negative_image_data = pars_data(negative_img, new_buffer)

        obj = Image.objects.create(
            base64=negative_image_data[1],
            path=ContentFile(negative_image_data[0], name="negative_img.jpeg")
        )

        return ImageNegativeMutation(obj)


class ImageCompressionMutation(relay.ClientIDMutation):
    class Input:
        base64 = graphene.String(required=True)
        quality = graphene.Int(required=True)

    image = graphene.Field(ImageType)

    @classmethod
    @prepare_image
    def mutate_and_get_payload(cls, root, info, **kwargs):
        quality = kwargs.get('quality')
        new_buffer = BytesIO()
        kwargs.get('pillow_img').save(
            new_buffer,
            format='JPEG',
            optimize=True,
            quality=quality
        )

        compressed_img_str = base64.b64encode(new_buffer.getvalue()).decode('utf-8')
        compressed_img_data = base64.b64decode(compressed_img_str)

        obj = Image.objects.create(
            base64=compressed_img_str,
            path=ContentFile(compressed_img_data, name="compressed_img.jpeg")
        )

        return ImageCompressionMutation(obj)


class Mutation:
    resize_image = ImageResizeMutation.Field()
    crop_image = ImageCropMutation.Field()
    rotate_image = ImageRotateMutation.Field()
    negate_image = ImageNegativeMutation.Field()
    compress_image = ImageCompressionMutation.Field()
