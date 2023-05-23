import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
import boto3
import joblib
from io import BytesIO


app = FastAPI()



# Replace with your S3 bucket name
S3_BUCKET_NAME = "xxxx"

# Replace with your AWS access key ID and secret access key
s3 = boto3.client("s3", aws_access_key_id="xxxxxx", aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxx", region_name = 'eu-west-3')

region = s3.meta.region_name

S3_url = "https://netflix-project-bucket.s3.eu-west-3.amazonaws.com/mlflow/xxxxxxxxxxxxxxxxxxxxxxxxxxx/artifacts/model.pkl"
# Take only the name of the image
model_s3_key = S3_url.split('.com/')[1]

 # Load the model directly from S3 to BytesIO object
model_bytes = BytesIO()
s3.download_fileobj(S3_BUCKET_NAME, model_s3_key, model_bytes)

# Reset the file object position to the beginning
model_bytes.seek(0)

# Load the model from the BytesIO object
model = joblib.load(model_bytes)

@app.get("/")
async def index():

    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"

    return message


@app.get("/get-model")
async def get_svd_model(user_id, movie_id):

    return round(model.predict(user_id, movie_id).est, 3)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)
