# MFA Copilot Docker & Kubernetes Deployment

## Docker

Build and run locally:

```bash
docker build -t mfa-copilot:latest .
docker run --rm -p 8501:8501 -e GROQ_API_KEY=your_key mfa-copilot:latest
```

Or with Docker Compose:

```bash
export GROQ_API_KEY=your_key
docker compose up --build
```

Open http://localhost:8501

## Kubernetes

1. Create/update the secret:

```bash
kubectl create secret generic mfa-copilot-secrets \
  --from-literal=groq-api-key="$GROQ_API_KEY" \
  --dry-run=client -o yaml | kubectl apply -f -
```

2. Apply storage and workload:

```bash
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

3. For a local cluster such as minikube, load the image first:

```bash
minikube image load mfa-copilot:latest
```

4. Check rollout:

```bash
kubectl get pods,svc,pvc
```

5. Get the external address:

```bash
kubectl get svc mfa-copilot
```
