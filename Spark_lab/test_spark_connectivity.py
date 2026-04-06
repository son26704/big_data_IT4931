#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Spark Lab Connectivity Test
Tests connection to Spark cluster and basic functionality
"""

import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import time

def test_spark_connection():
    """Test basic Spark cluster connectivity"""
    print("🔧 Testing Spark cluster connectivity...")
    
    try:
        # Initialize Spark Session
        spark = SparkSession.builder \
            .appName("SparkConnectivityTest") \
            .master("spark://localhost:7077") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()
        
        # Set log level to reduce verbosity
        spark.sparkContext.setLogLevel("WARN")
        
        print("✅ Spark Session created successfully!")
        print("📊 Spark Version: {}".format(spark.version))
        print("🔗 Master URL: {}".format(spark.sparkContext.master))
        print("📱 App Name: {}".format(spark.sparkContext.appName))
        
        # Test basic functionality
        print("\n🧪 Testing basic Spark functionality...")
        
        # Test 1: Create simple DataFrame
        print("   📊 Test 1: Creating DataFrame...")
        test_data = [(1, "Alice", 25), (2, "Bob", 30), (3, "Charlie", 35)]
        df = spark.createDataFrame(test_data, ["id", "name", "age"])
        
        print("   📊 DataFrame created with {} records".format(df.count()))
        df.show()
        
        # Test 2: Basic transformations
        print("\n   🔄 Test 2: DataFrame transformations...")
        transformed_df = df.filter(col("age") > 25).select("name", "age")
        result_count = transformed_df.count()
        
        print("   ✅ Transformation completed: {} records".format(result_count))
        transformed_df.show()
        
        # Test 3: Aggregations
        print("\n   📊 Test 3: Aggregations...")
        avg_age = df.agg(avg("age")).collect()[0][0]
        print("   ✅ Average age: {}".format(avg_age))
        
        # Test 4: Cluster information
        print("\n🔍 Cluster Information:")
        sc = spark.sparkContext
        executor_infos = sc.statusTracker().getExecutorInfos()
        
        print("   🔧 Active Executors: {}".format(len(executor_infos)))
        for executor in executor_infos:
            print("      Executor {}: {}:{}".format(executor.executorId, executor.host, executor.port))
        
        # Test 5: Performance test
        print("\n⚡ Performance Test:")
        start_time = time.time()
        
        # Create larger dataset for performance test
        large_data = [(i, "User_{}".format(i), 20 + (i % 50)) for i in range(1000)]
        large_df = spark.createDataFrame(large_data, ["id", "name", "age"])
        
        # Perform aggregation
        result = large_df.groupBy("age").count().collect()
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print("   ⏱️ Processed 1000 records in {:.3f} seconds".format(processing_time))
        print("   📊 Found {} unique ages".format(len(result)))
        
        # Cleanup
        spark.stop()
        print("\n✅ Spark cluster connectivity test completed successfully!")
        return True
        
    except Exception as e:
        print("\n❌ Spark cluster connectivity test failed: {}".format(e))
        print("\n💡 Troubleshooting tips:")
        print("   - Make sure Spark cluster is running: docker compose up -d")
        print("   - Check if localhost:7077 is accessible")
        print("   - Verify Docker containers are healthy")
        print("   - Check network connectivity between containers")
        return False

def test_kafka_connection():
    """Test Kafka connectivity for streaming"""
    print("\n🔧 Testing Kafka connectivity...")
    
    try:
        from kafka import KafkaProducer, KafkaConsumer
        import json
        
        # Test Kafka producer
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Send test message
        test_message = {"test": "connectivity", "timestamp": time.time()}
        future = producer.send('test-topic', test_message)
        producer.flush()
        
        print("✅ Kafka producer connection successful!")
        
        # Test Kafka consumer
        consumer = KafkaConsumer(
            'test-topic',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            consumer_timeout_ms=1000
        )
        
        print("✅ Kafka consumer connection successful!")
        
        producer.close()
        consumer.close()
        
        print("✅ Kafka connectivity test completed!")
        return True
        
    except Exception as e:
        print("❌ Kafka connectivity test failed: {}".format(e))
        print("\n💡 Troubleshooting tips:")
        print("   - Make sure Kafka is running: docker compose up -d")
        print("   - Check if localhost:9092 is accessible")
        print("   - Verify Kafka containers are healthy")
        return False

def main():
    """Main test function"""
    print("🚀 Spark Lab Connectivity Test")
    print("=" * 50)
    
    # Test Spark connectivity
    spark_success = test_spark_connection()
    
    # Test Kafka connectivity
    kafka_success = test_kafka_connection()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    print("   🔧 Spark Cluster: {} PASS".format("✅" if spark_success else "❌"))
    print("   📡 Kafka: {} PASS".format("✅" if kafka_success else "❌"))
    
    if spark_success and kafka_success:
        print("\n🎉 All connectivity tests passed!")
        print("🚀 Ready to start Spark Lab experiments!")
    else:
        print("\n⚠️ Some connectivity tests failed.")
        print("🔧 Please fix the issues before proceeding.")
    
    return spark_success and kafka_success

if __name__ == "__main__":
    main()
