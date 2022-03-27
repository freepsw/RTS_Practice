# Apache Kafka Producer & Consumer 구현 (Python)
- Python library (confluent-kafka)를 활용한 구현
- https://github.com/confluentinc/confluent-kafka-python
- https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent-kafka-api


## 개발환경 구성
```
> mkdir ~/python_kafka
> cd ~/python_kafka 

# python 3 가상환경 생성
> sudo yum install -y python3 
> python3 -m venv kafka_virtualenv

## 가상환경 실행하기 
> source kafka_virtualenv/bin/activate
> python -V

# kafka library 설치 
> pip install --upgrade pip
> pip install confluent-kafka==1.8.2  
```

### kafka 환경 구성
### Create a topic
```
> cd $KAFKA_HOME
> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic my_topic
```

## Basic Producer/Consumer/Admin code 
### Basic Producer Test 
#### Run the kafka console consumer
```
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my_topic --from-beginning
```

#### Run the python (Producer)
```
> cd ~/python_kafka 
> source kafka_virtualenv/bin/activate

## python code 작성
> vi producer.py

## 메시지 전송 후 consumer에서 정상 수신하는지 확인 
> python producer.py
Message delivered to my_topic [1]
```

### Basic Consumer Test 
#### Run the python (Consumer)
```
> cd ~/python_kafka 
> source kafka_virtualenv/bin/activate

## python code 작성
> vi consumer.py

## 메시지 전송 후 consumer에서 정상 수신하는지 확인 
> python consumer.py
Received message: test-msg
```


### Basic Kafka Admin Test
#### Create a topic (my_topic_admin)
```
> cd ~/python_kafka 
> source kafka_virtualenv/bin/activate

> vi admin.py 

> python admin.py 
Topic my_topic_new1 created
Topic my_topic_new2 created

> cd $KAFKA_HOME
> bin/kafka-topics.sh --list --bootstrap-server localhost:9092
my_topic_new1
my_topic_new2

```

## Advanced Producer/Consumer/Admin code 
### Consumer  code
```
> cd ~/python_kafka 
> source kafka_virtualenv/bin/activate

> vi consumer_detail.py 

> python consumer_detail.py localhost my_group my_topic

Assignment: [TopicPartition{topic=my_topic,partition=0,offset=-1001,error=None}, TopicPartition{topic=my_topic,partition=1,offset=-1001,error=None}]
% my_topic [1] at offset 0 with key None:
b'test-msg'
% my_topic [1] at offset 1 with key None:
b'test-msg'
% my_topic [1] at offset 2 with key None:
b'test-msg'
% my_topic [1] at offset 3 with key None:
b'test-msg'
% my_topic [0] at offset 0 with key None:
b'test-msg'
```

### Producer code
```
> cd ~/python_kafka 
> source kafka_virtualenv/bin/activate

> vi producer_detail.py 

> python producer_detail.py localhost my_topic
new msg
my msg
% Message delivered to my_topic [0] @ 1
```
- consumer에서 정상적으로 수신하는지 확인한다. 

### Producer Key/Value Code 
```
> cd ~/python_kafka 
> source kafka_virtualenv/bin/activate

> vi producer_key.py 

> python producer_key.py 

> python producer_key.py
Message delivered to my_topic [0]
Message delivered to my_topic [0]
Message delivered to my_topic [0]
.....
```


## 가상환경 종료하기 
```
> deactivate
```


## ETC 

### Anaconda vs. Miniconda vs. Virtualenv
- https://deeplearning.lipingyang.org/2018/12/23/anaconda-vs-miniconda-vs-virtualenv/
- https://stackoverflow.com/questions/38217545/what-is-the-difference-between-pyenv-virtualenv-anaconda

#### Anaconda
- python과 관련된 모든 어플리케이션, 패키지 등을 자동으로 설치
- 약 720개 이상의 package들을 자동으로 설치해 줌. 
- 최소 3G 이상의 디스크 공간 필요  

#### Miniconda 
- python package를 관리하기 위한 용도로 최적화
- Anaconda에서 제공하는 다양한 어플리케이션은 설치되지 않음
- 단순히 python 가상환경을 구성하여 프로그래밍하는 목적으로 최적
- 디스크 사용량 최소화 (다만 필요한 패키지는 직접 설치)

##### Virtualenv
- python 버전별로 별도의 python 가상환경을 제공하는 용도
    - pyenv는 python 버전 별로 환경을 제공했다면, (동일 package의 다른 버전 설치시 관리 어려움)
    - virtualenv는 동일한 python 버전이라도,
    - 프로젝트에 따라 동일한 package의 다른 버전을 설치할 수 있도록 지원
- sudo(관리자 권한)이 있는 경우에만 사용 가능함. 
- conda 보다 복잡한 명령어 이해와 관리가 필요

#### pyenv
- python 버전을 쉽게 설치 및 변경할 수 있게 지원
- 동일한 버전의 python에 서로 다른 버전의 package(numpy 등)을 설치하면
- 버전 호환등의 문제로 실행시 오류가 발생하는 이슈 (사용자가 직접 관리해야 함)
    - 즉, 완벽한 독립적인 가상환경을 제공하지는 못함. 
- windows는 지원하지 않음

#### Example virtualenv for python3
```shell
> pip install virtualenv
> virtualenv venv_ --python=python3.8
> source venv/bin/activate
> python -m pip install --upgrade pip
> 
```