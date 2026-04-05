# Kafka Lab cho người mới: setup và bắt đầu thực hành (Ubuntu + VS Code + root .venv)

Tài liệu này viết riêng cho bạn với bối cảnh hiện tại:

- Hệ điều hành: Ubuntu
- IDE: VS Code
- Môi trường Python: root `.venv` ở thư mục gốc repo
- Không dùng conda/Anaconda
- Chưa muốn agent tự chạy full lab

Mục tiêu của tài liệu: giúp bạn hiểu bản chất Kafka từ đầu, chuẩn bị đúng môi trường cho Kafka Lab, và biết chính xác các lệnh cần chạy khi bạn tự bắt đầu thực hành.

## Phần A - Kafka là gì, giải thích từ đầu

### 1) Streaming data là gì?

Streaming data là dữ liệu đi vào hệ thống liên tục theo thời gian, từng sự kiện một hoặc theo các cụm nhỏ, thay vì gom thành file lớn rồi xử lý một lần.

Ví dụ:

- Giá cổ phiếu cập nhật mỗi giây
- Log ứng dụng phát sinh liên tục
- Click người dùng trên website/app

### 2) Real-time data là gì?

Real-time data là dữ liệu được thu thập và xử lý gần như ngay lập tức khi nó xuất hiện. Không nhất thiết là "0 ms", mà là đủ nhanh để phục vụ quyết định gần thời gian thực.

### 3) Kafka dùng để làm gì?

Kafka là nền tảng event streaming. Bạn có thể hình dung Kafka là một "trục trung chuyển sự kiện":

- Producer gửi sự kiện vào Kafka
- Kafka lưu và phân phối sự kiện
- Consumer đọc sự kiện để xử lý

Kafka rất mạnh khi cần:

- Throughput cao
- Nhiều hệ thống cùng đọc một nguồn dữ liệu
- Tách rời producer và consumer (decouple)
- Có khả năng đọc lại dữ liệu theo offset (replay)

### 4) Các khái niệm cốt lõi

#### Broker

Một server Kafka. Broker nhận, lưu, và phục vụ message.

#### Topic

Kênh logic chứa message theo một chủ đề. Ví dụ topic `stock-data` chứa dữ liệu chứng khoán.

#### Producer

Thành phần gửi message vào topic.

#### Consumer

Thành phần đọc message từ topic.

#### Consumer Group

Một nhóm consumer cùng đọc một topic để chia tải. Trong cùng một group, một partition chỉ do một consumer xử lý tại một thời điểm.

#### Partition

Topic được chia thành nhiều partition để tăng khả năng scale và throughput.

#### Offset

Số thứ tự của message trong từng partition. Consumer dùng offset để biết đã đọc đến đâu.

### 5) Vì sao Kafka quan trọng trong Data Engineering?

Kafka thường là lớp ingest realtime trong pipeline:

- Thu nhận dữ liệu từ nhiều nguồn
- Đệm và tách nhịp giữa nguồn phát và hệ xử lý
- Cho phép nhiều downstream system tiêu thụ song song
- Hỗ trợ kiến trúc event-driven hiện đại

### 6) Kafka khác gì với app gọi API hoặc ghi thẳng DB?

API trực tiếp:

- Thường đồng bộ request-response
- Dễ phụ thuộc chặt giữa hai hệ thống

Ghi trực tiếp DB:

- Đơn giản lúc đầu, nhưng dễ nghẽn khi nhiều nguồn ghi/đọc

Kafka:

- Bất đồng bộ
- Decouple producer/consumer
- Linh hoạt mở rộng và replay
- Phù hợp bài toán event streaming

### 7) Khi nào nên dùng và không nên dùng Kafka?

Nên dùng khi:

- Cần ingest dữ liệu liên tục, volume lớn
- Cần fan-out cho nhiều consumer độc lập
- Cần xử lý gần realtime
- Cần khả năng replay dữ liệu

Không nên dùng khi:

- Bài toán nhỏ, đơn giản, tần suất thấp
- Chỉ cần queue nhẹ
- Team chưa sẵn sàng vận hành hệ thống phân tán

## Phần B - Kafka trong lab này hoạt động như thế nào

### 1) Lab mô phỏng bài toán gì?

Kafka Lab mô phỏng streaming dữ liệu thị trường chứng khoán (OHLCV) theo thời gian thực. Producer tạo dữ liệu cổ phiếu và gửi vào Kafka; consumer đọc để phân tích/giám sát.

### 2) Các thành phần trong Kafka Lab

Theo [Kafka_lab/docker-compose.yml](Kafka_lab/docker-compose.yml):

- `kafka` (Confluent Kafka 7.5.0, KRaft mode)
- `schema-registry`
- `kafka-connect`
- `akhq` (Kafka UI)
- `redis` (optional)

### 3) Data flow của lab

Luồng đơn giản:

1. Stock data generator / producer tạo message JSON
2. Producer gửi vào topic `stock-data`
3. Consumer hoặc nhiều consumer group đọc dữ liệu
4. Bạn quan sát topic/partition/consumer lag bằng AKHQ

### 4) Bạn sắp chạy những gì?

- Kiểm tra môi trường và preflight
- Cài package Python cần thiết trong root `.venv`
- Khởi động dịch vụ Docker theo thứ tự an toàn
- Chạy script test kết nối
- Mở notebook học từ lab 01 đến 05

### 5) Kết quả đầu ra mong đợi

- Kafka broker chạy ổn
- Producer gửi được message
- Consumer đọc được message
- AKHQ hiển thị topic, partition, message

### 6) Điểm cốt lõi và điểm phụ

Cốt lõi để học:

- Producer/consumer
- Topic/partition/offset
- Consumer group

Phụ trợ:

- Schema Registry
- Kafka Connect
- Redis
- AKHQ UI (hữu ích để quan sát)

### 7) Chỗ mâu thuẫn/cũ trong repo cần biết

- [Kafka_lab/SUMMARY.md](Kafka_lab/SUMMARY.md) còn mô tả stack có Zookeeper.
- Nhưng compose thực tế ở [Kafka_lab/docker-compose.yml](Kafka_lab/docker-compose.yml) đang dùng KRaft, không có Zookeeper.
- Khi có khác nhau, ưu tiên compose file hiện hành.

## Phần C - Môi trường của tôi và cách áp dụng

Bối cảnh của bạn:

- Ubuntu + VS Code
- Root `.venv` đã có và có kernel Jupyter
- Không dùng Anaconda/conda
- Docker chỉ bật khi cần

Áp dụng cho Kafka Lab:

1. Không cần dùng [Kafka_lab/setup_kafka_lab.sh](Kafka_lab/setup_kafka_lab.sh) vì script này ép conda env `datalab`.
2. Dùng root `.venv` + `pip install -r Kafka_lab/requirements.txt` là phù hợp.
3. Java host không bắt buộc để chạy Kafka container trong lab này (vì Kafka chạy trong Docker), nhưng có sẵn vẫn tốt cho tooling/debug.

## Phần D - Chuẩn bị trước khi chạy lab

### Bước 1: Mở đúng workspace và terminal

- Mở VS Code tại root repo
- Mở terminal tại root repo

### Bước 2: Kiểm tra và activate root `.venv`

- Xác nhận `.venv` tồn tại
- Activate `.venv`

### Bước 3: Kiểm tra Docker và Compose

- Docker daemon running
- Docker Compose dùng được

### Bước 4: Kiểm tra port Kafka thường dùng

Các port cần chú ý trong lab:

- 9092, 9093, 9101 (Kafka)
- 8080 (AKHQ)
- 8081 (Schema Registry)
- 8083 (Kafka Connect)
- 6379 (Redis optional)

### Bước 5: Kiểm tra compose/config

- Validate compose bằng `docker compose config --quiet`
- Chưa cần `up` full stack ở bước chuẩn bị

### Phân loại lệnh (rất quan trọng)

Lệnh chỉ đọc/kiểm tra:

- `docker compose config --quiet`
- `docker compose ps`
- `docker compose logs <service> --tail=50`
- `docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --list`

Lệnh làm thay đổi trạng thái service:

- `docker compose up -d ...`
- `docker compose down`
- `docker compose restart ...`

## Phần E - Các lệnh để bắt đầu thực hành

Lưu ý: đây là chuỗi lệnh để bạn tự chạy khi chính thức bắt đầu Kafka Lab.

### 1) Vào root repo

Command:

```bash
cd /home/son/Documents/IT4931_data_management_and_processing_lab_materials
```

Lệnh này làm gì: vào đúng thư mục gốc dự án.
Kỳ vọng: prompt đứng ở thư mục repo.
Lỗi phổ biến:

- `No such file or directory`: sai đường dẫn.

### 2) Activate root venv

Command:

```bash
source .venv/bin/activate
```

Lệnh này làm gì: bật môi trường Python riêng của repo.
Kỳ vọng: prompt có tiền tố `(.venv)`.
Lỗi phổ biến:

- `No such file`: chưa tạo `.venv` hoặc đang không ở root repo.

### 3) Vào Kafka_lab

Command:

```bash
cd Kafka_lab
```

Lệnh này làm gì: chuyển vào thư mục lab.
Kỳ vọng: prompt ở `.../Kafka_lab`.
Lỗi phổ biến:

- `No such file or directory`: đang đứng sai thư mục cha.

### 4) Cài package Python cho Kafka Lab

Command:

```bash
pip install -r requirements.txt
```

Lệnh này làm gì: cài dependency Python phục vụ notebook và test script Kafka.
Kỳ vọng: `Successfully installed ...` hoặc `Requirement already satisfied`.
Lỗi phổ biến:

- Permission error: chưa activate venv.
- Network timeout: lỗi mạng/proxy/PyPI.

### 5) Validate docker compose

Command:

```bash
docker compose config --quiet
```

Lệnh này làm gì: kiểm tra syntax/resolve compose.
Kỳ vọng: không in lỗi, exit code 0.
Lỗi phổ biến:

- YAML parse error: lỗi cú pháp compose.
- Docker daemon issue: Docker chưa chạy.

### 6) Khởi động Kafka broker trước

Command:

```bash
docker compose up -d kafka
```

Lệnh này làm gì: start broker trước để nền tảng ổn định.
Kỳ vọng: container `kafka_broker` chạy.
Lỗi phổ biến:

- `port is already allocated`: cổng bị chiếm.
- `permission denied /var/run/docker.sock`: thiếu quyền Docker.

### 7) Kiểm tra trạng thái broker

Command:

```bash
docker compose ps kafka
```

Lệnh này làm gì: kiểm tra service `kafka`.
Kỳ vọng: `Up` và sau một lúc có thể `healthy`.
Lỗi phổ biến:

- `Restarting`/`unhealthy`: cần xem logs.

### 8) Test broker bằng kafka-topics CLI

Command:

```bash
docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --list
```

Lệnh này làm gì: xác nhận broker trả lời lệnh quản trị topic.
Kỳ vọng: in danh sách topic (có thể trống lúc đầu).
Lỗi phổ biến:

- `Connection refused`: broker chưa sẵn sàng.

### 9) Khởi động dịch vụ phụ trợ

Command:

```bash
docker compose up -d schema-registry kafka-connect akhq
```

Lệnh này làm gì: bật service quan sát và tích hợp.
Kỳ vọng: các container phụ trợ `Up`.
Lỗi phổ biến:

- service phụ restart liên tục: kiểm tra logs và cấu hình bootstrap.

### 10) (Tuỳ chọn) bật Redis

Command:

```bash
docker compose up -d redis
```

Lệnh này làm gì: bật Redis nếu notebook/bài tập có dùng cache.
Kỳ vọng: `kafka_redis` chạy.
Lỗi phổ biến:

- cổng `6379` bị chiếm.

### 11) Kiểm tra toàn bộ stack hiện tại

Command:

```bash
docker compose ps
```

Lệnh này làm gì: xem tất cả service trong Kafka_lab.
Kỳ vọng: các service cần dùng đều `Up`.
Lỗi phổ biến:

- service `Exit`/`Restarting`: kiểm tra logs service đó.

### 12) Chạy test Python kết nối Kafka

Command:

```bash
python test_kafka.py
```

Lệnh này làm gì: test producer/consumer cơ bản với topic `stock-data`.
Kỳ vọng:

- `Producer test successful`
- `Consumer test successful`
  Lỗi phổ biến:
- `NoBrokersAvailable`: broker chưa sẵn sàng hoặc sai endpoint.
- timeout: service phụ thuộc chưa ổn định.

### 13) Mở Jupyter Lab và bắt đầu notebook

Command:

```bash
jupyter lab
```

Lệnh này làm gì: mở môi trường notebook.
Kỳ vọng: URL local Jupyter hiện ra.
Lỗi phổ biến:

- `jupyter: command not found`: jupyter chưa cài trong venv.

## Phần F - Cách đọc kết quả và tự kiểm tra hiểu bài

### 1) Khi lab chạy, nên quan sát gì?

- `docker compose ps`: service có `Up` ổn định không
- `docker compose logs kafka --tail=50`: broker có lỗi restart không
- AKHQ tại `http://localhost:8080`: topic, partition, message count, consumer group

### 2) Làm sao biết producer đang gửi dữ liệu?

- Script producer chạy không lỗi
- Message count trong topic tăng
- AKHQ thấy record mới

### 3) Làm sao biết consumer đang nhận dữ liệu?

- Consumer in record ra terminal
- Group offset tăng theo thời gian

### 4) Làm sao biết topic/partition hoạt động đúng?

- List topic thành công
- Topic có số partition như kỳ vọng
- Dữ liệu phân phối vào partition, và trong mỗi partition giữ thứ tự

### 5) Những hiểu lầm phổ biến của người mới

- Hiểu sai: offset là toàn topic.
  - Đúng: offset theo từng partition.
- Hiểu sai: cùng group, mọi consumer đều đọc cùng một message.
  - Đúng: trong cùng group, partition được chia cho các consumer.
- Hiểu sai: Kafka thay thế hoàn toàn database.
  - Đúng: Kafka là lớp event streaming, thường đi cùng DB/lake/warehouse.

## Phần G - Các lỗi hay gặp trên Ubuntu/VS Code/Docker

### 1) Docker daemon chưa chạy

Triệu chứng:

- `Cannot connect to the Docker daemon`

Cách xử lý:

- Bật Docker daemon, kiểm tra lại `docker info`.

### 2) Port bị chiếm

Triệu chứng:

- `bind: address already in use`

Cách xử lý:

- Dừng stack khác đang dùng cổng
- Hoặc đổi port mapping nếu cần

### 3) Container lên nhưng app không kết nối được

Triệu chứng:

- timeout, connection refused

Cách xử lý:

- Chờ service healthy
- Xem logs
- Kiểm tra endpoint/port

### 4) Nhầm `localhost` và hostname container

Quy tắc:

- Từ host chạy script: dùng `localhost:<mapped_port>`
- Từ container trong cùng compose network: dùng tên service

### 5) Venv không active

Triệu chứng:

- import lỗi dù đã cài package

Cách xử lý:

- activate `.venv`
- kiểm tra interpreter trong VS Code đúng venv

### 6) Java version issue

- Với lab Kafka dockerized này, Java host thường không phải blocker chính.
- Java host chủ yếu liên quan tooling chạy trực tiếp trên máy host.

### 7) File permission trên Ubuntu

Triệu chứng:

- permission denied với Docker socket hoặc volume

Cách xử lý:

- kiểm tra quyền user với Docker
- kiểm tra quyền thư mục bind mount

---

## Quyết định setup tối giản cho Kafka Lab (chốt)

- Dùng root `.venv` hiện tại, không cần tách venv riêng.
- Không dùng conda setup script của Kafka_lab.
- Cài package Python theo `Kafka_lab/requirements.txt` khi bắt đầu lab.
- Dùng Docker cho Kafka services, start theo thứ tự an toàn.
- Bước chuẩn bị chỉ cần preflight + hiểu kiến trúc, chưa cần chạy full lab ngay.
