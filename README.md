# MLOps Applied Lab — California Housing Predictor

An end-to-end MLOps project covering **experiment tracking, model registry, API deployment, Docker containerization, and Kubernetes orchestration** using MLflow, XGBoost, FastAPI, Docker, and Minikube.

## Project Overview

This project implements a complete machine learning deployment workflow for predicting California housing prices.

The project is divided into two main labs:

* **Lab 1:** Experiment Tracking with MLflow
* **Lab 2:** Model Deployment with FastAPI, Docker, and Kubernetes

## Architecture

```text
California Housing Dataset
          │
          ▼
     XGBoost Training
          │
          ▼
       MLflow
   Experiment Tracking
          │
          ▼
     Model Registry
          │
          ▼
   staging Model Alias
          │
          ▼
      model/ Artifact
          │
          ▼
       FastAPI
          │
          ▼
        Docker
          │
          ▼
      Minikube
          │
          ▼
    Kubernetes Deployment
       ┌──────┴──────┐
       ▼             ▼
     Pod 1         Pod 2
       └──────┬──────┘
              ▼
        Kubernetes Service
              │
              ▼
          /predict
```

## Lab 1 — Experiment Tracking with MLflow

The training pipeline uses the California Housing dataset from scikit-learn and trains three XGBoost configurations.

### Experiments

| Run       | Max Depth | Learning Rate | Validation RMSE |
| --------- | --------: | ------------: | --------------: |
| Run 1     |         3 |          0.10 |          0.5385 |
| **Run 2** |     **5** |      **0.05** |      **0.5221** |
| Run 3     |         7 |          0.01 |          0.7000 |

**Run 2** achieved the lowest validation RMSE and was selected as the best model.

The model was registered in MLflow as:

```text
California_Housing_Predictor
```

and assigned the:

```text
staging
```

alias.

### MLflow Configuration

The local MLflow tracking server uses SQLite as its backend store:

```bash
mlflow server \
  --backend-store-uri sqlite:///mlruns.db \
  --default-artifact-root ./artifacts \
  --host 127.0.0.1 \
  --port 5000
```

## Lab 2 — Model Deployment

The registered model was exported locally and served through a FastAPI application.

### API Endpoints

#### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

#### Prediction

```http
POST /predict
```

Example request:

```json
{
  "MedInc": 8.3252,
  "HouseAge": 41.0,
  "AveRooms": 6.9841,
  "AveBedrms": 1.0238,
  "Population": 322.0,
  "AveOccup": 2.5556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

Example response:

```json
{
  "prediction": "$430,082.66"
}
```

## Docker

The FastAPI application is containerized using Docker.

### Build

```bash
docker build -t california-housing-api:v1 .
```

### Run

```bash
docker run -d \
  --name housing-api \
  -p 8000:8000 \
  california-housing-api:v1
```

The API can then be accessed at:

```text
http://127.0.0.1:8000
```

## Kubernetes / Minikube

The application is deployed locally using Minikube.

The Kubernetes deployment contains:

* 2 replicas
* Kubernetes readiness probe
* Kubernetes Service
* LoadBalancer service type
* Local Docker image
* Port 8000 inside the containers

### Deploy

```bash
minikube start --driver=docker
```

Load the image into Minikube:

```bash
minikube image load california-housing-api:v1
```

Apply the Kubernetes resources:

```bash
kubectl apply -f k8s-deployment.yaml
```

Check the pods:

```bash
kubectl get pods
```

Expected result:

```text
housing-api-deployment-...   1/1   Running
housing-api-deployment-...   1/1   Running
```

### Access the Service

The service can be accessed locally using:

```bash
minikube service housing-api-service --url
```

or with port forwarding:

```bash
kubectl port-forward svc/housing-api-service 8080:80
```

## Project Structure

```text
mlops-california-housing/
│
├── train.py
├── app.py
├── requirements.txt
├── requirements-deployment.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── k8s-deployment.yaml
├── model/
│   ├── MLmodel
│   ├── model.ubj
│   ├── conda.yaml
│   ├── python_env.yaml
│   ├── registered_model_meta
│   └── requirements.txt
└── README.md
```

## Technologies Used

* Python
* XGBoost
* Scikit-learn
* MLflow
* FastAPI
* Pydantic
* Pandas
* NumPy
* Docker
* Kubernetes
* Minikube
* SQLite
* Git & GitHub

## MLOps Workflow

The project demonstrates the following workflow:

```text
Train
  ↓
Track Experiments
  ↓
Compare Models
  ↓
Register Best Model
  ↓
Assign Model Alias
  ↓
Export Model
  ↓
Build FastAPI Service
  ↓
Containerize with Docker
  ↓
Deploy with Kubernetes
  ↓
Expose Prediction API
```

## Notes

The project uses separate dependency files for the training/tracking environment and the deployment environment.

The deployment environment follows the dependency versions specified by the lab guide.

## Author

**Mohamed El-Sharqawy**

Data Science & AI Student
Menofia University

GitHub: [mohamedel-sharqawy](https://github.com/mohamedel-sharqawy)
