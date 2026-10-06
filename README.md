# 🔁 CI/CD With Rollback

Pipeline that tests, builds, deploys — and automatically rolls back if the new version fails health checks.

## Pipeline Flow
```
git push main
    ↓
1. Test       — pytest (fails here = no deploy)
    ↓
2. Build      — Docker image → Docker Hub (tagged with SHA)
    ↓
3. Deploy     — docker run new version
    ↓
4. Health     — curl /health (6 retries × 5s = 30s window)
    ↓
5a. Pass  ✅  → Deployment complete
5b. Fail  ❌  → Rollback to previous image automatically
```

## Simulate a bad deploy
Set `FORCE_FAIL=true` env var — /health returns 500 → rollback triggers:
```bash
# Locally
docker run -e FORCE_FAIL=true -e APP_VERSION=bad-v2 -p 5000:5000 youruser/cicd-rollback-app:latest
curl http://localhost:5000/health  # Returns 500
```

## GitHub Secrets needed
| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

## Key learning
- Health check window: 6 attempts × 5s = 30 seconds to confirm healthy
- Rollback records previous image before deploying new one
- Tests must pass before build — broken code never reaches Docker Hub
