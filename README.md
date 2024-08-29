# QR Scan with API and image upload to S3

This project is a small proof of concept of how an API could receive QR images over HTTP, process them and upload them to S3, without the need to use the file system.

It is also possible to retrieve an image previously scanned and uploaded to S3 by its data.

[FastAPI](https://fastapi.tiangolo.com/) is used for the API and as a local alternative to AWS S3 [minio](https://min.io/docs/minio/linux/reference/minio-server/minio-server.html)

## Run in local

To run the application locally just download the repository and run `docker compose up -d --build`

Once running you can make use of the api from its documentation section [http://localhost:8000/docs](http://localhost:8000/docs).

You can also consult the contents of the bucket with the web interface from [http://localhost:9001/browser](http://localhost:9001/browser).
Credentials for minio webpage are `qrtest` and `simplepass`, `qr-bucket` is the default bucket.

## Test

You can test the application from the web interfaces mentioned above or also from the terminal by executing the following command:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/image' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@resource/qr_code.png;type=image/png'
```

Which should return the following `{"type":"QRCODE","data":"123456789"}`