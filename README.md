# Bloc_7
**Data engineering project**

This project aims at :  
- creating a recommendation engine,
- creating an infrastructure that ingest real-time user interactions on the platform,
- automatically producing real-time recommendations after a user finished a movie

Contact : Lise Gnos  
email : lise.gnos@gmail.com  

This is a team project that was done in collaboration with Nizar Sayad and Christian Segnou.  

## 1/ Training

> Folder : 'TRAIN'  

The dataset was taken from Netflix prize data, available at this url : https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data?datasetId=1636&sortBy=voteCount&select=movie_titles.csv

First the preprocessings were done.  
Then the model (SVD) was trained with a gridsearch. Parallelization was used with Ray and Kubernetes on GCP. The model was logged to MLFlow with an artifact store on a S3 bucket.  

## 2/ API

> Folder : 'API'  

The final trained model was put in the API made with FastAPI in order to be called for predictions.

## 3/ Streaming

> Folder : 'STREAMING'  

A producer and a consumer scripts were made, using Kafka and Confluent Cloud.  
The producer calls an API in order to simulate real-time user interaction with the platform. The producer sends the data from the API to the consumer.  
The consumer calls the model from the API with the received information in order to make the predictions.  
The predictions are stored in a postgres database.

## 4/ Web dashboard

> Folder : 'WEBAPP'  

A web application was made with Streamlit in order to show the recommendations in real-time.  

👉 The API and Web application were dockerised and deployed respectively on an EC2 instance and on Heroku.  


