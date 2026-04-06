# Spark Lab cho Beginner (Ubuntu + VS Code + root .venv)

Tài liệu này là bản hướng dẫn thực chiến cho học viên mới, ưu tiên:

- Dùng Ubuntu local
- Dùng VS Code
- Dùng Python `venv` + `pip` tại root repo
- Không dùng Conda
- Không chạy full stack ngay từ đầu

Phạm vi:

- Chuẩn bị môi trường đủ để bắt đầu Spark Lab
- Chạy theo từng bước nhỏ, có kiểm tra sau mỗi bước
- Chưa yêu cầu chạy toàn bộ tất cả notebook trong một lần

---

## A) Spark Lab này dạy gì?

Spark Lab trong repo tập trung vào 6 hướng chính:

1. Batch processing với DataFrame API
2. Structured Streaming (rate source và Kafka)
3. Spark SQL
4. Machine Learning cơ bản với MLlib
5. Tích hợp Iceberg (nâng cao)
6. Tích hợp Kafka producer/consumer với Spark

Mục tiêu học tập thực tế:

- Hiểu cách Spark phân tán công việc qua Master/Worker
- Viết transform/aggregation trên dữ liệu vừa và lớn
- Phân biệt batch vs streaming
- Biết khi nào cần thêm thành phần nâng cao (Kafka, Iceberg, ML)

---

## B) Mức độ khó và lộ trình học khuyến nghị

### Mức độ theo notebook

- `01_spark_batch_processing.ipynb`: Dễ -> Trung bình (nền tảng)
- `04_spark_sql.ipynb`: Dễ -> Trung bình (nền tảng quan trọng)
- `02_spark_streaming.ipynb`: Trung bình (thêm khái niệm stream, trigger, checkpoint)
- `06_spark_kafka_integration.ipynb`: Trung bình -> Khó (thêm Kafka)
- `03_spark_ml.ipynb`: Trung bình (optional với Data Engineer)
- `05_spark_iceberg_integration.ipynb`: Khó (nâng cao, phụ thuộc thêm JAR/package)

### Lộ trình cho beginner

1. `01_spark_batch_processing.ipynb`
2. `04_spark_sql.ipynb`
3. `02_spark_streaming.ipynb`
4. `06_spark_kafka_integration.ipynb`
5. `03_spark_ml.ipynb` (tùy chọn)
6. `05_spark_iceberg_integration.ipynb` (để sau cùng)

Lý do:

- Batch + SQL giúp nắm DataFrame, Catalyst, execution plan trước.
- Streaming/Kafka cần nền batch vững để debug được.
- Iceberg là phần tích hợp nhiều lớp, dễ quá tải nếu học sớm.

---

## C) Chuẩn bị môi trường (Ubuntu + VS Code + root .venv)

### 1. Kích hoạt môi trường Python root

Từ root repo:

```bash
source .venv/bin/activate
python -m pip install -U pip
```

### 2. Cài gói theo 2 pha

Pha tối thiểu (đủ chạy 01/04/02 cơ bản):

```bash
python -m pip install pyspark findspark pyarrow pandas numpy matplotlib seaborn jupyter ipykernel kafka-python
```

Pha mở rộng (khi cần 03/06/05):

```bash
python -m pip install scikit-learn mlflow confluent-kafka psycopg2-binary sqlalchemy
```

Gợi ý: nếu máy yếu hoặc mạng chậm, cài pha tối thiểu trước.

### 3. Đăng ký kernel venv cho notebook

```bash
python -m ipykernel install --user --name it4931-root-venv --display-name "Python (it4931-root-venv)"
```

Trong VS Code/Jupyter, chọn kernel: `Python (it4931-root-venv)`.

### 4. Chuẩn bị Docker cho Spark cluster

```bash
cd Spark_lab
docker compose pull
```

Trước khi `up`, đảm bảo không có stack khác đang chiếm cổng 8080/8081/8083/8888/9092/5432/6379.

Ví dụ nếu đang chạy Kafka Lab:

```bash
cd ../Kafka_lab
docker compose down
cd ../Spark_lab
```

### 5. Khởi động dịch vụ Spark Lab theo hướng incremental

```bash
docker compose up -d spark-master spark-worker-1 spark-worker-2 kafka schema-registry postgres redis
```

Không bắt buộc khởi động `jupyter-spark` container nếu bạn dùng VS Code + kernel local.

### 6. Kiểm tra nhanh connectivity

```bash
python test_spark_connectivity.py
```

Kỳ vọng:

- Spark connect tới `spark://localhost:7077`
- Kafka connect tới `localhost:9092`

---

## D) Các mismatch đã xử lý để phù hợp workflow beginner

Các chỉnh sửa tối thiểu đã áp dụng vào mã nguồn Spark Lab:

1. `Spark_lab/docker-compose.yml`

- Thêm `healthcheck` cho Kafka.
- Sửa Schema Registry bootstrap sang `kafka:9092` (endpoint nội bộ docker network).

2. `Spark_lab/setup_spark_lab.sh`

- Bỏ luồng conda-first, ưu tiên môi trường Python đang active (`venv` khuyến nghị).
- Dùng `python3 -m pip install -r requirements.txt`.
- Mẫu `.env` đổi endpoint theo host (`localhost`) để chạy notebook local dễ hơn.
- Dùng cú pháp `docker compose`.

3. `Spark_lab/README.md`

- Mẫu environment variables chuyển sang `localhost` cho luồng host-based.
- Thêm ghi chú: nếu chạy trong docker network thì dùng hostname nội bộ (`spark-master`, `kafka`, `postgres`, `redis`).

4. `Spark_lab/notebooks/*.ipynb`

- Chuẩn hóa Spark master endpoint sang `spark://localhost:7077` để phù hợp notebook chạy local kernel.
- `01_spark_batch_processing.ipynb` được sửa cell khởi tạo Spark để không ép `SparkContext('local')`.

5. `Spark_lab/test_spark_connectivity.py`

- Cập nhật thông báo troubleshooting theo endpoint host (`localhost`).

---

## E) Quy trình chạy notebook theo từng chặng

### Chặng 1: Nền tảng batch + SQL

- Mở `01_spark_batch_processing.ipynb`.
- Chạy từng cell, kiểm tra Spark Session tạo thành công.
- Chú ý các thao tác: `filter`, `groupBy`, `agg`, `join`, `orderBy`.

Sau đó:

- Mở `04_spark_sql.ipynb`.
- Tập trung `createOrReplaceTempView`, SQL query, explain plan.

Mục tiêu chặng 1:

- Nắm được DataFrame API và Spark SQL tương đương nhau ra sao.

### Chặng 2: Streaming cơ bản

- Mở `02_spark_streaming.ipynb`.
- Chạy phần rate source trước (không cần Kafka ngay).
- Khi ổn định mới chạy phần Kafka stream.

Mục tiêu chặng 2:

- Hiểu trigger interval, watermark/window, checkpoint.

### Chặng 3: Kafka integration

- Mở `06_spark_kafka_integration.ipynb`.
- Tạo topic, producer test, rồi đọc stream từ Spark.
- Verify dữ liệu bằng consumer riêng.

Mục tiêu chặng 3:

- Nắm end-to-end flow: produce -> process -> sink.

### Chặng 4: Optional nâng cao

- `03_spark_ml.ipynb`: làm khi muốn ôn ML pipeline.
- `05_spark_iceberg_integration.ipynb`: làm sau cùng, chuẩn bị thêm package/JAR tương thích.

---

## F) Troubleshooting nhanh

### 1. Không connect được Spark master

Triệu chứng:

- Lỗi khi tạo SparkSession, timeout hoặc connection refused.

Checklist:

- `docker compose ps` trong `Spark_lab`.
- Kiểm tra port 7077 đã expose.
- Đảm bảo notebook dùng `spark://localhost:7077` (luồng host).

### 2. Không connect được Kafka

Triệu chứng:

- Producer/consumer báo broker unavailable.

Checklist:

- `docker compose ps` và Kafka ở trạng thái healthy.
- Endpoint phía host phải là `localhost:9092`.
- Không chạy song song Kafka của lab khác.

### 3. Cổng bị chiếm

Triệu chứng:

- `port is already allocated` khi `docker compose up`.

Checklist:

- Dừng stack lab trước đó (`docker compose down` ở lab tương ứng).
- Kiểm tra container đang chạy bằng `docker ps`.

### 4. Notebook chạy sai kernel

Triệu chứng:

- Thiếu package dù đã cài.

Checklist:

- Verify kernel đang là `Python (it4931-root-venv)`.
- Trong terminal cùng kernel: `python -m pip show pyspark`.

### 5. Iceberg notebook lỗi package/JAR

Triệu chứng:

- `ClassNotFoundException` hoặc lỗi catalog.

Checklist:

- Hoãn notebook Iceberg đến cuối lộ trình.
- Chốt version Spark-Iceberg tương thích trước khi chạy lại.

---

## G) Kiến thức then chốt cần nắm sau khi hoàn thành Spark Lab cơ bản

1. Spark execution model

- Driver, Executor, Cluster Manager
- Lazy evaluation, lineage, action vs transformation

2. DataFrame và SQL optimizer

- Tối ưu query nhờ Catalyst + Tungsten
- Partitioning và shuffle là nguồn chi phí chính

3. Structured Streaming

- Micro-batch model
- Exactly-once/at-least-once phụ thuộc source/sink/checkpoint

4. Spark + Kafka integration

- Offset management
- Throughput vs latency trade-off

5. Kỷ luật vận hành khi học lab

- Chỉ chạy một stack tại một thời điểm
- Chạy từ dễ đến khó, luôn có checkpoint kiểm chứng

---

## Lệnh mẫu end-to-end (không full lab, chỉ preflight)

```bash
# 1) root repo
source .venv/bin/activate
python -m pip install -U pip

# 2) nếu cần cài tối thiểu Spark libs
python -m pip install pyspark findspark pyarrow pandas numpy matplotlib seaborn jupyter ipykernel kafka-python

# 3) chuyển Spark lab
cd Spark_lab

# 4) tắt stack cũ nếu có (thực hiện ở lab cũ tương ứng)
# cd ../Kafka_lab && docker compose down && cd ../Spark_lab

# 5) khởi động dịch vụ cần thiết
docker compose up -d spark-master spark-worker-1 spark-worker-2 kafka schema-registry postgres redis

# 6) kiểm tra nhanh connectivity
python test_spark_connectivity.py
```

Nếu tới đây đều PASS, bạn đã sẵn sàng vào notebook theo lộ trình ở mục B/E.
