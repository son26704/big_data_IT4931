# Kafka Lab Quick Checklist (Ubuntu + VS Code + root .venv)

Checklist nhanh trước khi bắt đầu Kafka Lab.

## 1) Toolchain

- [ ] Docker daemon đang chạy
- [ ] Docker Compose dùng được
- [ ] VS Code mở đúng workspace repo
- [ ] Internet ổn định để pull image và cài package

## 2) Ports

- [ ] Các cổng sau đang rảnh: 9092, 9093, 9101, 8080, 8081, 8083
- [ ] Cổng 6379 rảnh nếu bạn bật Redis (optional)

## 3) Python root .venv

- [ ] `.venv` tồn tại ở root repo
- [ ] Đã `source .venv/bin/activate`
- [ ] Python đúng venv
- [ ] Đã cài dependency Kafka Lab: `pip install -r Kafka_lab/requirements.txt`
- [ ] Không dùng conda cho workflow này

## 4) Docker Compose validation

- [ ] `cd Kafka_lab`
- [ ] `docker compose config --quiet` pass
- [ ] Có thể start broker trước: `docker compose up -d kafka`
- [ ] Broker lên ổn: `docker compose ps kafka`

## 5) Ready-to-start actions

- [ ] Test broker: `docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --list`
- [ ] Start service phụ: `docker compose up -d schema-registry kafka-connect akhq`
- [ ] Optional Redis: `docker compose up -d redis`
- [ ] Test Python: `python test_kafka.py`
- [ ] Mở AKHQ: http://localhost:8080
- [ ] Mở notebook theo thứ tự 01 -> 05

## 6) Nhắc nhanh lỗi phổ biến

- Docker daemon chưa chạy
- Port bị chiếm
- Venv chưa active
- Nhầm `localhost` (host) và hostname service (container network)
- Script `setup_kafka_lab.sh` yêu cầu conda nên không dùng trong workflow hiện tại
