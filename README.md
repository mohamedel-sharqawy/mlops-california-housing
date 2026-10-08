\# MLOps Applied Lab — California Housing Predictor



An end-to-end MLOps project covering \*\*experiment tracking, model registry, API deployment, Docker containerization, and Kubernetes orchestration\*\* using MLflow, XGBoost, FastAPI, Docker, and Minikube.



\## Project Overview



This project implements a complete machine learning deployment workflow for predicting California housing prices.



The project is divided into two main labs:



\* \*\*Lab 1:\*\* Experiment Tracking with MLflow

\* \*\*Lab 2:\*\* Model Deployment with FastAPI, Docker, and Kubernetes



\## Architecture



```text

California Housing Dataset

&#x20;         │

&#x20;         ▼

&#x20;    XGBoost Training

&#x20;         │

&#x20;         ▼

&#x20;      MLflow

&#x20;  Experiment Tracking

&#x20;         │

&#x20;         ▼

&#x20;    Model Registry

&#x20;         │

&#x20;         ▼

&#x20;  staging Model Alias

&#x20;         │

&#x20;         ▼

&#x20;     model/ Artifact

&#x20;         │

&#x20;         ▼

&#x20;      FastAPI

&#x20;         │

&#x20;         ▼

&#x20;       Docker

&#x20;         │

&#x20;         ▼

&#x20;     Minikube

&#x20;         │

&#x20;         ▼

&#x20;   Kubernetes Deployment

&#x20;      ┌──────┴──────┐

&#x20;      ▼             ▼

&#x20;    Pod 1         Pod 2

&#x20;      └──────┬──────┘

&#x20;             ▼

&#x20;       Kubernetes Service

&#x20;             │

&#x20;             ▼

&#x20;         /predict

```



\## Lab 1 — Experiment Tracking with MLflow



The training pipeline uses the California Housing dataset from scikit-learn and trains three XGBoost configurations.



\### Experiments



| Run       | Max Depth | Learning Rate | Validation RMSE |

| --------- | --------: | ------------: | --------------: |

| Run 1     |         3 |          0.10 |          0.5385 |

| \*\*Run 2\*\* |     \*\*5\*\* |      \*\*0.05\*\* |      \*\*0.5221\*\* |

| Run 3     |         7 |          0.01 |          0.7000 |



\*\*Run 2\*\* achieved the lowest validation RMSE and was selected as the best model.



The model was registered in MLflow as:



```text

California\_Housing\_Predictor

```



and assigned the:



```text

staging

```



alias.



\### MLflow Configuration



The local MLflow tracking server uses SQLite as its backend store:



```bash

mlflow server \\

&#x20; --backend-store-uri sqlite:///mlruns.db \\

&#x20; --default-artifact-root ./artifacts \\

&#x20; --host 127.0.0.1 \\

&#x20; --port 5000

```



\## Lab 2 — Model Deployment



The registered model was exported locally and served through a FastAPI application.



\### API Endpoints



\#### Health Check



```http

GET /health

```



Example response:



```json

{

&#x20; "status": "healthy"

}

```



\#### Prediction



```http

POST /predict

```



Example request:



```json

{

&#x20; "MedInc": 8.3252,

&#x20; "HouseAge": 41.0,

&#x20; "AveRooms": 6.9841,

&#x20; "AveBedrms": 1.0238,

&#x20; "Population": 322.0,

&#x20; "AveOccup": 2.5556,

&#x20; "Latitude": 37.88,

&#x20; "Longitude": -122.23

}

```



Example response:



```json

{

&#x20; "prediction": "$430,082.66"

}

```



\## Docker



The FastAPI application is containerized using Docker.



\### Build



```bash

docker build -t california-housing-api:v1 .

```



\### Run



```bash

docker run -d \\

&#x20; --name housing-api \\

&#x20; -p 8000:8000 \\

&#x20; california-housing-api:v1

```



The API can then be accessed at:



```text

http://127.0.0.1:8000

```



\## Kubernetes / Minikube



The application is deployed locally using Minikube.



The Kubernetes deployment contains:



\* 2 replicas

\* Kubernetes readiness probe

\* Kubernetes Service

\* LoadBalancer service type

\* Local Docker image

\* Port 8000 inside the containers



\### Deploy



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



\### Access the Service



The service can be accessed locally using:



```bash

minikube service housing-api-service --url

```



or with port forwarding:



```bash

kubectl port-forward svc/housing-api-service 8080:80

```



\## Project Structure



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

│   ├── python\_env.yaml

│   ├── registered\_model\_meta

│   └── requirements.txt

└── README.md

```



\## Technologies Used



\* Python

\* XGBoost

\* Scikit-learn

\* MLflow

\* FastAPI

\* Pydantic

\* Pandas

\* NumPy

\* Docker

\* Kubernetes

\* Minikube

\* SQLite

\* Git \& GitHub



\## MLOps Workflow



The project demonstrates the following workflow:



```text

Train

&#x20; ↓

Track Experiments

&#x20; ↓

Compare Models

&#x20; ↓

Register Best Model

&#x20; ↓

Assign Model Alias

&#x20; ↓

Export Model

&#x20; ↓

Build FastAPI Service

&#x20; ↓

Containerize with Docker

&#x20; ↓

Deploy with Kubernetes

&#x20; ↓

Expose Prediction API

```



\## Notes



The project uses separate dependency files for the training/tracking environment and the deployment environment.



The deployment environment follows the dependency versions specified by the lab guide.



\## Author



\*\*Mohamed El-Sharqawy\*\*



Data Science \& AI Student

Menofia University



GitHub: \[mohamedel-sharqawy](https://github.com/mohamedel-sharqawy)



