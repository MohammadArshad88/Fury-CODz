from flask import Flask, request, jsonify, send_file
import boto3
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
import json
from flask import Flask
from flask_cors import CORS, cross_origin
import base64

app = Flask(__name__)
cors = CORS(app, resource={r"/": {"origins": ""}})

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def home():
  return "Hello, World!"


# AWS credentials and configuration
AWS_ACCESS_KEY_ID = 'AKIAXJXXKU5EAU3U2JMJ'  #ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = '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'  #SECRET_ACCESS_KEY
AWS_REGION = 'ap-southeast-2'  #AWS_REGION
S3_BUCKET_NAME = 'speciesinfostorage'  #S3 BUCKET NAME
DYNAMODB_TABLE_NAME = 'SpeciesInformation'  #DYNAMODB TABLE NAME
REKOGNITION_MAX_LABELS = 1
POLLY_VOICE_ID = 'Joanna'  # You can change the voice ID as needed

# Initializing AWS clients
s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION)
rekognition_client = boto3.client('rekognition',
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  region_name=AWS_REGION)
dynamodb_client = boto3.client('dynamodb',
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                               region_name=AWS_REGION)
polly_client = boto3.client('polly',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION)


# Function to get species information from DynamoDB
def detect_labels_and_annotate(image_bytes):
  detect_objects = rekognition_client.detect_labels(
      Image={'Bytes': image_bytes},
      MaxLabels=
      1  # Set MaxLabels to 1 to get only the label with the highest confidence
  )

  image = Image.open(io.BytesIO(image_bytes))
  draw = ImageDraw.Draw(image)

  for label in detect_objects['Labels']:
    print(label["Name"])
    print("Confidence: ", label["Confidence"])

    # Ensure there are instances and BoundingBox in the label
    if 'Instances' in label and label['Instances']:
      for instances in label['Instances']:
        if 'BoundingBox' in instances:
          box = instances["BoundingBox"]

          left = image.width * box['Left']
          top = image.height * box['Top']
          width = image.width * box['Width']
          height = image.height * box['Height']

          points = [(left, top), (left + width, top),
                    (left + width, top + height), (left, top + height),
                    (left, top)]
          draw.line(points, width=5, fill="#69f5d9")

          shape = [(left - 2, top - 35), (width + 2 + left, top)]
          draw.rectangle(shape, fill="#69f5d9")

          font = ImageFont.load_default()

          text_x = left
          text_y = top - 40  # Adjust the vertical position as needed

          draw.text((text_x, text_y), label["Name"], font=font, fill='#000000')

          # Use Amazon Polly to announce the label
          # announce_label_with_polly(f"{label['Name']}")

  return image, f"{label['Name']}"

