# ☁️ GCP Serverless Function — Python

A production-ready **Google Cloud Function (Gen 2)** written in Python, with:
- ✅ Local development via `functions-framework`
- ✅ Unit tests with `pytest`
- ✅ VS Code debug & launch configs
- ✅ GitHub Actions CI/CD pipeline → auto-deploy on `main`

---

## 📁 Project Structure

```
gcp-serverless-python/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── .vscode/
│   ├── settings.json           # Python, linting, formatting
│   ├── launch.json             # Run/debug locally
│   └── extensions.json         # Recommended extensions
├── src/
│   ├── main.py                 # ← Cloud Function entry point
│   └── requirements.txt        # Runtime dependencies
├── tests/
│   └── test_main.py            # Unit tests
├── requirements.txt            # Dev + runtime dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start (Local)

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/YOUR_USERNAME/gcp-serverless-python.git
cd gcp-serverless-python

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Run Locally

```bash
cd src
functions-framework --target hello_cloud --port 8080 --debug
```

Test it:
```bash
# GET
curl "http://localhost:8080?name=YourName"

# POST
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "data": {"foo": "bar"}}'
```

### 3. Run Tests

```bash
pytest tests/ -v --cov=src
```

---

## ☁️ GCP Setup (One-Time)

### Step 1 — Create a GCP Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project, note your **Project ID**
3. Enable these APIs:
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   ```

### Step 2 — Create a Service Account

```bash
# Create service account
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub Actions Deployer"

# Grant required roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.developer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Generate JSON key
gcloud iam service-accounts keys create gcloud-service-key.json \
  --iam-account=github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

---

## 🔐 GitHub Secrets Setup

Go to your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name     | Value                                      |
|-----------------|--------------------------------------------|
| `GCP_PROJECT_ID`| Your GCP Project ID (e.g. `my-project-123`)|
| `GCP_SA_KEY`    | Full contents of `gcloud-service-key.json` |

> ⚠️ **Never commit `gcloud-service-key.json` to Git!** It's in `.gitignore`.

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) runs on every push:

```
Push to any branch  →  Run Tests + Lint
Push to main        →  Run Tests + Lint → Deploy to GCP → Smoke Test
```

**Pipeline steps:**
1. 🧪 Lint with `flake8`, format-check with `black`
2. 🧪 Run `pytest` (requires ≥80% coverage)
3. 🚀 Authenticate to GCP using service account key
4. 🚀 Deploy Cloud Function (Gen 2) with `gcloud functions deploy`
5. ✅ Smoke test the live endpoint

---

## ⚙️ Customising Your Function

Edit `src/main.py` to add your logic. The entry point is:

```python
@functions_framework.http
def hello_cloud(request):
    # Your code here
    ...
```

To change the function name, update:
- `--entry-point` in `deploy.yml`
- `FUNCTION_NAME` env var in `deploy.yml`

---

## 🛠️ VS Code Tips

- **Run locally**: Press `F5` → select "▶ Run Cloud Function Locally"
- **Debug tests**: Press `F5` → select "🧪 Run Pytest"
- Install recommended extensions when prompted (`.vscode/extensions.json`)

---

## 📦 Deploy Manually (optional)

```bash
gcloud functions deploy hello-cloud \
  --gen2 \
  --region=us-central1 \
  --runtime=python311 \
  --source=./src \
  --entry-point=hello_cloud \
  --trigger-http \
  --allow-unauthenticated
```
