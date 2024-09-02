import cv2
import numpy as np
import uvicorn

from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import StreamingResponse
from pyzbar.pyzbar import decode
from config import s3_client, S3_BUCKET
from middleware import log_middleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

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
    
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        proxy_headers=True,
        forwarded_allow_ips='*',
        access_log=False)