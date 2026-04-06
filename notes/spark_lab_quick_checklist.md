# Spark Lab Quick Checklist (Beginner)

## 0) Scope

- [ ] Học Spark_lab theo workflow Ubuntu + VS Code + root `.venv`
- [ ] Không chạy full lab ngay
- [ ] Chỉ chạy một Docker stack tại một thời điểm

## 1) Python Environment

- [ ] `source .venv/bin/activate`
- [ ] `python -m pip install -U pip`
- [ ] Cài tối thiểu:
  - [ ] `pyspark`
  - [ ] `findspark`
  - [ ] `pyarrow`
  - [ ] `pandas`, `numpy`
  - [ ] `jupyter`, `ipykernel`
  - [ ] `kafka-python`

## 2) Kernel Notebook

- [ ] `python -m ipykernel install --user --name it4931-root-venv --display-name "Python (it4931-root-venv)"`
- [ ] Trong notebook, chọn đúng kernel `Python (it4931-root-venv)`

## 3) Docker Preflight

- [ ] Tắt stack lab cũ nếu đang chạy (`docker compose down` ở lab đó)
- [ ] Vào thư mục Spark lab: `cd Spark_lab`
- [ ] `docker compose pull`
- [ ] `docker compose up -d spark-master spark-worker-1 spark-worker-2 kafka schema-registry postgres redis`

## 4) Smoke Test

- [ ] `python test_spark_connectivity.py`
- [ ] Spark PASS (`spark://localhost:7077`)
- [ ] Kafka PASS (`localhost:9092`)

## 5) Học Theo Thứ Tự

- [ ] `01_spark_batch_processing.ipynb`
- [ ] `04_spark_sql.ipynb`
- [ ] `02_spark_streaming.ipynb`
- [ ] `06_spark_kafka_integration.ipynb`
- [ ] `03_spark_ml.ipynb` (optional)
- [ ] `05_spark_iceberg_integration.ipynb` (advanced, làm sau)

## 6) Nếu lỗi, kiểm tra nhanh

- [ ] Cổng xung đột: 8080/8081/8083/8888/9092/5432/6379
- [ ] Kafka không healthy -> chờ thêm rồi thử lại
- [ ] Sai kernel -> package báo thiếu dù đã cài
- [ ] Notebook endpoint phải là host mode (`localhost`) khi chạy local kernel
