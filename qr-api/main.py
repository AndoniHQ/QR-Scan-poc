import cv2
import os
import numpy as np
import boto3

from io import BytesIO
from botocore.client import Config
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from pyzbar.pyzbar import decode

S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_PORT = os.environ.get("S3_PORT")
S3_USER = os.environ.get("S3_USER")
S3_PASS = os.environ.get("S3_PASS")
S3_BUCKET = os.environ.get("S3_BUCKET")

s3_client = boto3.client(
    's3',
    endpoint_url=f"http://{S3_ENDPOINT}:{S3_PORT}",
    aws_access_key_id=S3_USER,
    aws_secret_access_key=S3_PASS,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

app = FastAPI()

@app.get("/health")
async def health_check():
    try:
        s3_client.list_objects_v2(Bucket=S3_BUCKET)
        return {"status": "healthy", "bucket": "Available"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Bucket is not accesible: {str(e)}"
        )

@app.post("/api/image")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    np_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    barcode = decode(image)

    if barcode:
        barcode = barcode[0]
        barcode_info = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        s3_client.put_object(Bucket=S3_BUCKET, Key=f"{barcode_info}.png", Body=contents)
        return {"type": barcode_type, "data": barcode_info}
    
    return {"message": "Barcode not detected."}

@app.get("/images/{barcode}")
async def get_image(barcode: str):
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=f"{barcode}.png")
        image_data = response['Body'].read()

        return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")
    
    except s3_client.exceptions.NoSuchKey:
        return {"message": "Image not found"}