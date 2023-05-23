from ray.job_submission import JobSubmissionClient

job_submitter = JobSubmissionClient(address="http://127.0.0.1:8265")
job_id = job_submitter.submit_job(
    entrypoint="python train1.py",
    runtime_env={
        "working_dir": "./",
        "pip": ["numpy", "joblib", "scikit-learn", "scikit-surprise", "mlflow"],
        # Environment variables for our MLFlow sample app server 👇
        "env_vars": {
            "MLFLOW_EXPERIMENT_ID": "1",
            "MLFLOW_TRACKING_URI": "https://xxxxxxxxx",
            "AWS_ACCESS_KEY_ID": "xxxxxxxxxxxxxx",
            "AWS_SECRET_ACCESS_KEY": "xxxxxxxxxxxxxxxxxx",
            "BACKEND_STORE_URI": "postgresql://xxxxxxxxxxxxxxxxxxxxxx@ec2-54-234-13-16.compute-1.amazonaws.com:5432/xxxxxxxxxxxxx",
            "ARTIFACT_STORE_URI": "s3://xxxxxxxxxxxxxxx/",
             }
    }
)
print(f"Job submitted with id: {job_id}")
