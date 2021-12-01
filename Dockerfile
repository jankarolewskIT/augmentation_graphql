FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=augmented_img_API.settings
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN mkdir test_image