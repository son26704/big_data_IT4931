# IT4931 Progress

## Current Phase

- [x] Repository scan and setup analysis completed.
- [x] Minimal Ubuntu + venv baseline initialized.
- [x] Kafka Lab preparation docs for beginner workflow created.
- [ ] First lab not started yet.

## Environment Baseline (2026-04-04)

- Python: 3.10.12
- System pip: not available (`python3 -m pip` missing)
- Virtual env: `.venv` at repository root
- Git: 2.34.1
- Docker: 29.3.1
- Docker Compose: v5.1.1
- Java: OpenJDK 21.0.10
- Jupyter kernel: `IT4931 venv`

## Decisions

- Use Python `venv` + `pip` as primary workflow.
- Do not run all lab setup scripts blindly.
- Do not start heavy stacks until lab-specific learning starts.
- Keep Docker verification lightweight in this phase.

## Next Actions

- Start Kafka Lab preflight and install Kafka-specific Python dependencies in root `.venv`.
- Start Kafka services in safe order (broker first, then supporting services).
- Run `Kafka_lab/test_kafka.py`, then begin notebooks from 01 to 05.
