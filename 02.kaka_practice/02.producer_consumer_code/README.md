# Apache Kafka Producer & Consumer 구현 


## Python library (confluent-kafka)를 활용한 구현
- https://github.com/confluentinc/confluent-kafka-python
### 개발환경 구성
```
> mkdir ~/python_kafka
> cd ~/python_kafka 

# python 3 가상환경 생성
> sudo yum install -y python3 
> python3 -m venv kafka_virtualenv
> source kafka_virtualenv/bin/activate
> python -V

# kafka library 설치 
> pip install --upgrade pip
> pip install confluent-kafka==1.8.2  
> ==0.5.0
```


> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic my_topic