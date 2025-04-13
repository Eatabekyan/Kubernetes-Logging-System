#!/bin/bash

echo "Building Docker image..."
docker build -t custom-app:latest ./app

echo "Applying Kubernetes configurations..."
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/daemonset.yaml
kubectl apply -f kubernetes/cronjob.yaml

echo "Waiting for deployments to be ready..."
kubectl rollout status deployment/app-deployment

echo -e "\nService Information:"
kubectl get service app-service

pkill -f "port-forward" 
kubectl port-forward svc/app-service 8080:80 &

echo "Deployment completed!" 