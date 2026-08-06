# Exercise 5 — Helm Charts

## Objective

Learn how Helm templating works by converting plain YAML manifests into parameterized Helm templates.

## Background

This directory contains a Helm chart for a Notes application with three components:

- **frontend** — A Flask web UI (already fully templated with Go syntax)
- **backend** — A Flask API that stores notes in PostgreSQL (plain hardcoded YAML)
- **db** — A PostgreSQL database (plain hardcoded YAML)

The frontend templates in `templates/frontend-*.yaml` use Go template syntax (`{{ .Values.frontend.* }}`), pulling values from `values.yaml`. The backend and database templates are currently plain YAML with hardcoded values — your job is to convert them.

## Tasks

### Part 1 — Explore the Chart

1. Look at `values.yaml` — notice it only has frontend values
2. Look at `templates/frontend-deployment.yaml` — this is what a properly templated manifest looks like
3. Compare with `templates/backend-deployment.yaml` — notice the hardcoded values

### Part 2 — Template the Backend

1. Add backend configuration to `values.yaml` (image, replicas, resources, service port, DB connection details)
2. Convert `templates/backend-deployment.yaml` to use `{{ .Values.backend.* }}` references
3. Convert `templates/backend-service.yaml` to use template values

### Part 3 — Template the Database

1. Add database configuration to `values.yaml` (image, replicas, resources, credentials, storage size)
2. Convert `templates/db-deployment.yaml`, `templates/db-service.yaml`, and `templates/db-secret.yaml` to use template values

### Part 4 — Deploy

1. Install the chart: `helm install my-notes . -n <your-namespace>`
2. Verify all three pods are running and the app works
3. Try overriding a value: `helm upgrade my-notes . --set frontend.replicaCount=2 -n <your-namespace>`

## Useful Commands

```bash
helm template . --debug          # Preview rendered manifests without installing
helm install <name> . -n <ns>    # Install the chart
helm upgrade <name> . -n <ns>    # Apply changes
helm list -n <ns>                # List installed releases
helm uninstall <name> -n <ns>    # Remove the release
```
