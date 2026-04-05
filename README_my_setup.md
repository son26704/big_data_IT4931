# My Setup Notes for IT4931

## Goal

Create a stable, lightweight learning environment on Ubuntu using existing Python + `venv` + `pip`, with Docker used on demand.

## What Was Set Up

1. Verified host toolchain.
2. Created root virtual environment: `.venv`.
3. Installed minimal packages in `.venv`:
   - `jupyterlab`
   - `ipykernel`
   - `pandas`
   - `requests`
   - `python-dotenv`
4. Registered kernel: `IT4931 venv`.
5. Checked common lab ports: no listeners found at setup time.

## Current Policy

- Install lab dependencies only when starting that lab.
- Avoid running multiple lab Docker stacks simultaneously.
- Avoid full-stack setup scripts unless specifically needed.

## Quick Commands

```bash
cd /home/son/Documents/IT4931_data_management_and_processing_lab_materials
source .venv/bin/activate
jupyter lab
```

## Deferred Until Lab Start

- Airflow local Python package stack
- dbt + Great Expectations full toolchain
- Spark/Kafka heavy local Python dependencies
- Kubernetes local cluster (minikube/kind)
