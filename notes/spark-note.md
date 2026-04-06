Tuyệt vời! Sau khi hoàn thành Kafka, bạn đang bước vào **Apache Spark** – một trong những nền tảng xử lý dữ liệu mạnh mẽ nhất trong hệ sinh thái Big Data. Vì bạn muốn học từ con số 0, mình sẽ trình bày một cách **đầy đủ, dễ hiểu, có minh họa và không giả định bạn đã biết trước**.

---

# 1. Apache Spark là gì?

## 📌 Định nghĩa

**Apache Spark** là một nền tảng xử lý dữ liệu phân tán mã nguồn mở, được thiết kế để xử lý dữ liệu lớn (Big Data) với tốc độ cao và khả năng mở rộng mạnh mẽ.

Spark có thể xử lý:

* Dữ liệu batch (xử lý theo lô)
* Dữ liệu streaming (dòng thời gian thực)
* Machine Learning
* Phân tích dữ liệu
* Xử lý đồ thị

---

## 📊 Spark dùng để làm gì?

| Ứng dụng              | Ví dụ                                 |
| --------------------- | ------------------------------------- |
| Phân tích dữ liệu lớn | Phân tích hành vi người dùng          |
| Xử lý log             | Phân tích log hệ thống                |
| Data Engineering      | ETL từ Data Lake                      |
| Machine Learning      | Huấn luyện mô hình dự đoán            |
| Streaming             | Xử lý dữ liệu từ Kafka                |
| BI & Dashboard        | Cung cấp dữ liệu cho Power BI/Tableau |

---

# 2. Vì sao Spark ra đời?

Trước Spark, Hadoop MapReduce là tiêu chuẩn xử lý dữ liệu lớn. Tuy nhiên, MapReduce có nhược điểm:

| Hadoop MapReduce              | Apache Spark              |
| ----------------------------- | ------------------------- |
| Chậm do đọc/ghi đĩa nhiều lần | Nhanh nhờ xử lý trong RAM |
| Khó lập trình                 | API đơn giản              |
| Chỉ xử lý batch               | Hỗ trợ batch và streaming |
| Không phù hợp cho ML          | Có thư viện ML tích hợp   |

👉 Spark nhanh hơn Hadoop MapReduce đến **100 lần trong bộ nhớ**.

---

# 3. Kiến trúc của Apache Spark

## 🏗️ Tổng quan

```
User Application
        │
        ▼
    Spark Driver
        │
        ▼
    Cluster Manager
        │
        ▼
   Worker Nodes
        │
        ▼
      Executors
        │
        ▼
        Tasks
```

---

## 3.1 Các thành phần chính

### 🔹 Driver

* Là bộ não của ứng dụng Spark.
* Chịu trách nhiệm:

  * Lập kế hoạch thực thi
  * Tạo DAG (Directed Acyclic Graph)
  * Điều phối các task

### 🔹 Cluster Manager

Quản lý tài nguyên của cluster.

Các loại phổ biến:

* Standalone
* YARN
* Kubernetes
* Mesos

### 🔹 Worker Nodes

Các máy tính trong cụm cluster thực thi công việc.

### 🔹 Executors

* Chạy trên worker nodes.
* Thực thi các task và lưu dữ liệu trung gian trong bộ nhớ.

### 🔹 Tasks

* Đơn vị công việc nhỏ nhất trong Spark.
* Mỗi partition tương ứng với một task.

---

# 4. Luồng hoạt động của Spark

Giả sử bạn chạy đoạn code:

```python
df = spark.read.csv("data.csv")
result = df.filter(df.age > 30).groupBy("city").count()
result.show()
```

### 🔄 Quy trình thực thi

1. **SparkSession nhận lệnh**
2. **Driver tạo DAG**
3. **Catalyst Optimizer tối ưu hóa**
4. **Chia dữ liệu thành partitions**
5. **Cluster Manager cấp tài nguyên**
6. **Executors xử lý dữ liệu song song**
7. **Kết quả được trả về**

---

# 5. Khái niệm cốt lõi của Spark

## 5.1 Resilient Distributed Dataset (RDD)

RDD là cấu trúc dữ liệu nền tảng của Spark.

### Đặc điểm:

* Phân tán
* Bất biến (Immutable)
* Chịu lỗi (Fault-tolerant)
* Xử lý song song

### Ví dụ:

```python
rdd = spark.sparkContext.parallelize([1, 2, 3, 4])
rdd.map(lambda x: x * 2).collect()
```

---

## 5.2 Transformations và Actions

### 🔹 Transformations (Lazy)

Không thực thi ngay.

| Transformation | Ý nghĩa            |
| -------------- | ------------------ |
| map()          | Áp dụng hàm        |
| filter()       | Lọc dữ liệu        |
| flatMap()      | Trải phẳng dữ liệu |
| groupByKey()   | Nhóm dữ liệu       |
| reduceByKey()  | Tổng hợp dữ liệu   |

Ví dụ:

```python
rdd2 = rdd.map(lambda x: x * 2)
```

---

### 🔹 Actions

Kích hoạt việc thực thi.

| Action           | Ý nghĩa               |
| ---------------- | --------------------- |
| collect()        | Lấy dữ liệu về Driver |
| count()          | Đếm                   |
| take()           | Lấy một phần          |
| saveAsTextFile() | Lưu dữ liệu           |

Ví dụ:

```python
rdd2.collect()
```

---

## 5.3 Lazy Evaluation

Spark chỉ thực thi khi gặp Action.

```
map → filter → groupBy → count
                │
             (Action)
```

Điều này giúp Spark tối ưu hóa toàn bộ pipeline.

---

# 6. Directed Acyclic Graph (DAG)

Spark không dùng MapReduce. Thay vào đó, nó dùng DAG.

### Ví dụ:

```python
rdd.map(...).filter(...).reduce(...)
```

DAG:

```
Input → Map → Filter → Reduce → Output
```

Spark tối ưu hóa DAG trước khi thực thi.

---

# 7. DataFrame và Dataset

## 7.1 DataFrame

DataFrame giống bảng trong SQL hoặc Pandas.

```python
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df.show()
```

### Ưu điểm:

* Nhanh hơn RDD
* Có Catalyst Optimizer
* Hỗ trợ SQL

---

## 7.2 Dataset

* Kiểu dữ liệu an toàn (type-safe).
* Chủ yếu dùng trong Scala/Java.
* Python không hỗ trợ Dataset thực thụ.

---

# 8. Spark SQL

Cho phép truy vấn dữ liệu bằng SQL.

```python
df.createOrReplaceTempView("people")
spark.sql("SELECT * FROM people WHERE age > 30").show()
```

---

# 9. Spark Structured Streaming

Spark hỗ trợ xử lý dữ liệu thời gian thực.

### Ví dụ đọc từ Kafka:

```python
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stock-topic") \
    .load()
```

---

# 10. Hệ sinh thái của Spark

| Thư viện             | Chức năng         |
| -------------------- | ----------------- |
| Spark Core           | Xử lý dữ liệu     |
| Spark SQL            | Phân tích dữ liệu |
| Structured Streaming | Streaming         |
| MLlib                | Machine Learning  |
| GraphX               | Phân tích đồ thị  |

---

# 11. Fault Tolerance trong Spark

Spark phục hồi dữ liệu thông qua **lineage**.

Nếu một partition bị mất, Spark tính toán lại từ nguồn gốc thay vì lưu bản sao.

---

# 12. Partitioning

Spark chia dữ liệu thành nhiều phần để xử lý song song.

```
Dataset → Partition 1
        → Partition 2
        → Partition 3
```

Số partition ảnh hưởng trực tiếp đến hiệu năng.

---

# 13. Tối ưu hiệu năng trong Spark

| Kỹ thuật           | Mục đích              |
| ------------------ | --------------------- |
| Cache/Persist      | Lưu dữ liệu trong RAM |
| Repartition        | Tăng số partition     |
| Coalesce           | Giảm số partition     |
| Broadcast Join     | Tối ưu join           |
| Catalyst Optimizer | Tối ưu truy vấn       |
| Tungsten Engine    | Tối ưu bộ nhớ         |

---

# 14. So sánh Spark với Kafka

| Kafka                     | Spark                   |
| ------------------------- | ----------------------- |
| Streaming platform        | Processing engine       |
| Lưu trữ và truyền dữ liệu | Phân tích dữ liệu       |
| Producer/Consumer         | Transformations/Actions |
| Topic/Partition           | Dataset/Partition       |

👉 Kafka cung cấp dữ liệu, Spark xử lý dữ liệu.

---

# 15. Ví dụ Pipeline Kafka + Spark

```
Data Source → Kafka → Spark Streaming → Data Lake → Dashboard
```

---

# 16. Ví dụ hoàn chỉnh bằng PySpark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkExample") \
    .getOrCreate()

data = [("Alice", 34), ("Bob", 29), ("Charlie", 40)]
df = spark.createDataFrame(data, ["Name", "Age"])

df.filter(df.Age > 30).show()
```

Output:

```
+-------+---+
| Name  |Age|
+-------+---+
| Alice |34 |
|Charlie|40 |
+-------+---+
```

---

# 17. Tóm tắt toàn bộ kiến thức

| Khái niệm            | Ý nghĩa                       |
| -------------------- | ----------------------------- |
| Spark                | Engine xử lý dữ liệu phân tán |
| Driver               | Điều phối ứng dụng            |
| Executor             | Thực thi task                 |
| RDD                  | Cấu trúc dữ liệu gốc          |
| DataFrame            | Dữ liệu dạng bảng             |
| Transformation       | Phép biến đổi                 |
| Action               | Kích hoạt tính toán           |
| DAG                  | Kế hoạch thực thi             |
| Lazy Evaluation      | Tính toán trì hoãn            |
| Catalyst             | Bộ tối ưu SQL                 |
| Tungsten             | Tối ưu hiệu năng              |
| Structured Streaming | Xử lý dữ liệu thời gian thực  |

---

# 18. Lộ trình học Spark đề xuất

Vì bạn đã học Kafka, lộ trình phù hợp sẽ là:

1. **Giới thiệu PySpark và SparkSession**
2. **RDD và Transformations**
3. **DataFrame và Spark SQL**
4. **Joins và Window Functions**
5. **Spark Optimization**
6. **Structured Streaming**
7. **Spark + Kafka Integration**
8. **Xây dựng dự án hoàn chỉnh**

---

# 19. Bạn đã sẵn sàng cho notebook

Khi bạn gửi notebook Spark đầu tiên, mình sẽ:

* giải thích từng cell code
* phân tích output
* liên hệ với Kafka khi cần
* chỉ ra insight và best practices

---

Nếu bạn muốn, mình có thể tạo thêm:

* sơ đồ tư duy (mindmap),
* cheat sheet PDF,
* hoặc bộ câu hỏi ôn tập về Spark.

Hãy gửi **Lab Spark đầu tiên** để chúng ta bắt đầu! 🚀
