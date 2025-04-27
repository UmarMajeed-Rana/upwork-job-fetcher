```markdown
# upwork-job-fetcher

This repository contains a simple Flask application that fetches Upwork job postings. The Dockerfile provided lets you build and run the app locally, and deploy it to Google Cloud Run under the existing GCP project **`upwork-433522`** (service name: `upwork-job-fetcher`, region: `us-central1`).

---

## 📋 Prerequisites

- **Docker** (v20+)
- **gcloud CLI** (installed & authenticated: `gcloud auth login`)
- **GCP Project**: `upwork-433522`
  - Cloud Run API enabled  
  - You have the `run.admin` and `storage.admin` roles (or equivalent)
- **Billing** enabled for the project

---

## 🏗 Building the Docker Image

From the project root (where your `Dockerfile` lives), run:

```bash
docker build -t upwork-job-fetcher .
```

This will:

1. Pull the official `python:3.11-slim` image  
2. Copy your source into `/app`  
3. Install dependencies from `requirements.txt`  
4. Expose port `8080`

---

## ▶️ Running Locally

Once the build completes:

```bash
docker run \
  --name upwork-job-fetcher-local \
  -e FLASK_APP=app/main.py \
  -p 8080:8080 \
  upwork-job-fetcher
```

- The app will be available at <http://localhost:8080>  
- To stop & remove:
  ```bash
  docker stop upwork-job-fetcher-local
  docker rm upwork-job-fetcher-local
  ```

---

## ☁️ Pushing to Google Container Registry (GCR)

1. **Tag** your local image:

   ```bash
   docker tag upwork-job-fetcher \
     gcr.io/upwork-433522/upwork-job-fetcher:latest
   ```

2. **Authenticate** Docker to GCR (if not done already):

   ```bash
   gcloud auth configure-docker
   ```

3. **Push**:

   ```bash
   docker push gcr.io/upwork-433522/upwork-job-fetcher:latest
   ```

---

## 🚀 Deploying to Cloud Run

Update (or create) the Cloud Run service named `upwork-job-fetcher` in `us-central1`:

```bash
gcloud run deploy upwork-job-fetcher \
  --image gcr.io/upwork-433522/upwork-job-fetcher:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

- **--allow-unauthenticated** makes the service public. Omit it if you need IAM-protected access.  
- To update environment variables or CPU/memory settings, add flags like `--set-env-vars`, `--memory`, or `--concurrency`.

---

## 🔧 Environment Variables

| Variable      | Description                    | Default             |
|---------------|--------------------------------|---------------------|
| `FLASK_APP`   | entrypoint module for Flask    | `app/main.py`       |
| `PORT`        | port the app listens on        | `8080`              |
| (any others)  | e.g. API keys, timeouts, etc.  |                     |

You can set them in Cloud Run via:
```bash
gcloud run services update upwork-job-fetcher \
  --update-env-vars KEY1=VALUE1,KEY2=VALUE2 \
  --region us-central1
```

---

## 🧹 Cleaning Up

- **Delete Cloud Run service**:
  ```bash
  gcloud run services delete upwork-job-fetcher \
    --region us-central1
  ```
- **Remove pushed image**:
  ```bash
  gcloud container images delete \
    gcr.io/upwork-433522/upwork-job-fetcher:latest \
    --quiet
  ```

---

## 📚 Further Reading

- [Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts)
- [gcloud run deploy reference](https://cloud.google.com/sdk/gcloud/reference/run/deploy)
- [Managing Container Registry](https://cloud.google.com/container-registry/docs)
```


To update an existing Cloud Run service (rather than creating it for the first time), you can simply re-deploy with the new image and any revised settings. Cloud Run will detect that the service already exists and roll out a revision update.

```bash
# 1. Build & push a new image (if you haven’t already):
docker build -t upwork-job-fetcher .
docker tag upwork-job-fetcher \
  gcr.io/upwork-433522/upwork-job-fetcher:latest
docker push gcr.io/upwork-433522/upwork-job-fetcher:latest

# 2. Update the existing Cloud Run service:
gcloud run deploy upwork-job-fetcher \
  --image gcr.io/upwork-433522/upwork-job-fetcher:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated

# (Optional) 3. To change env vars, memory, or concurrency at the same time:
gcloud run deploy upwork-job-fetcher \
  --image gcr.io/upwork-433522/upwork-job-fetcher:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --update-env-vars KEY1=VALUE1,KEY2=VALUE2 \
  --memory 512Mi \
  --concurrency 80
```

- **`gcloud run deploy`** will automatically update (not recreate) the service if it already exists.  
- Any flags you pass (new image, env-vars, CPU/memory, concurrency, IAM settings) will be applied in the same command.  
- You can omit `--allow-unauthenticated` if you don’t want the service publicly reachable.