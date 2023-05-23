import pandas as pd
import numpy as np

from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

from surprise.model_selection import GridSearchCV

import ray
from ray.job_submission import JobSubmissionClient

import mlflow
from mlflow.models.signature import infer_signature

import joblib






df = pd.read_csv("https://netflix-project-bucket.s3.eu-west-3.amazonaws.com/data/processed_filtered_data.csv")



reader = Reader()

data = Dataset.load_from_df(df[['customer_id', 'movie_id', 'rating']], reader)


param_grid = {
    "n_epochs": [5, 10], 
    "lr_all": [0.002, 0.005], 
    "reg_all": [0.4, 0.6]
    }


gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=5)
gs.fit(data)


# best RMSE score
print("The best score of RMSE :", gs.best_score["rmse"])

# best MAE score
print("The best score of MAE : ", gs.best_score["mae"])

# combination of parameters that gave the best RMSE score
print("The best params of RMSE :", gs.best_params["rmse"])

# combination of parameters that gave the best RMSE score
print("The best params of MAE :", gs.best_params["mae"])


# Train the model with the best parameters
best_params_rmse = gs.best_params["rmse"]

model = SVD(**best_params_rmse)
trainset = data.build_full_trainset()
model.fit(trainset)


# Save the model as a file
model_file = "./model.pkl"
joblib.dump(model, model_file)

# Log metric with MLflow
with mlflow.start_run():
    # Log parameters and best score
    mlflow.log_metric('best_score_mae', gs.best_score["mae"])
    mlflow.log_metric('best_score_rmse', gs.best_score["rmse"])
    
    # Log parameters and rmse best params
    mlflow.log_params({'best_params_rmse': gs.best_params["rmse"]})
    mlflow.log_params({'best_params_mae': gs.best_params["mae"]})

    # Log the model file as an artifact
    mlflow.log_artifact(model_file)
    


