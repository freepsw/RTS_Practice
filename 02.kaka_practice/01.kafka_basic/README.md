# Apache Kafka 기본 명령어 활용 예시

## Set Kafka Home Directroy to user profile 
```
> echo "export KAFKA_HOME=~/apps/kafka_2.12-3.0.0" >> ~/.bash_profile
> source ~/.bash_profile
```

## 1. Basic Command 

### Key/Value 전송
```
> cd $KAFKA_HOME
> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic kv_topic

> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic kv_topic \
--property "parse.key=true" \
--property "key.separator=:" \
--property "print.key=true"
k1:msg1
k2:msg2
k3:msg3
k4:msg4
k5:msg5
k6:msg6
k7:msg7

> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic --from-beginning
msg1
msg2
msg3
msg4
msg5
msg6
msg7

> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic \
--property print.key=true \
--property key.separator="-" \
--group my-group \
--from-beginning
```

### Consumer Group 확인하기
```
> bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
my-group
console-consumer-60786

> bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe
Consumer group 'my-group' has no active members.

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID     HOST            CLIENT-ID
my-group        kv_topic        0          3               3               0               -               -               -
my-group        kv_topic        1          2               2               0               -               -               -
```


### Multi Consumer 실행
- my-group 내에 2개의 consumer를 실행한다. 
```
## Consumer 0 (my-group)
> cd $KAFKA_HOME
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic \
--property print.key=true \
--property key.separator="-" \
--group my-group \
--from-beginning

## Consumer 1 (my-group)
> cd $KAFKA_HOME
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic \
--property print.key=true \
--property key.separator="-" \
--group my-group \
--from-beginning

## Consumer group 확인 
## 2개의 consumer에 각 partition 1개씩 할당되어 처리하고 있음.  
> bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                              HOST            CLIENT-ID
my-group        kv_topic        1          5               5               0               consumer-my-group-1-af6d8bea-8022-4311-97f5-6f401a280b77 /10.146.0.2     consumer-my-group-1
my-group        kv_topic        0          9               9               0               consumer-my-group-1-ad09c671-39ba-47ec-b548-96d7ca9cdb5a /10.146.0.2     consumer-my-group-1

## Key/Value 데이터 전송 
## 동일한 Key 데이터가 항상 동일한 consumer로 전달 되는지 확인 가능 
> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic kv_topic \
--property "parse.key=true" \
--property "key.separator=:" \
--property "print.key=true"
k1:msg1
k2:msg2
k3:msg3
k4:msg4
k5:msg5
k1:msg1
k2:msg2
k3:msg3
k4:msg4
k5:msg5
k1:msg1
k2:msg2
```


### Consumer에서 특정 partition 데이터만 읽어오기
- partition 옵션을 통해서 특정 partition만 읽도록 조정 가능 
```
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic \
  --partition 1 \
  --from-beginning
```

### Consumer에서 특정 partition의 특정 offset 이후의 데이터만 읽어오기
- offset 0는 from-beginning과 동일한 효과 
```
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic \
  --partition 1 \
  --offset 0
```



## Idempotence Producer
```
> vi producer.conf
enable.idempotence=true
max.in.flight.request.per.connection=5
retries=3
acks=all

> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic kv_topic --producer.config producer.conf
```


### Delete messages in topic
- topic 내의 시작점에서 특정 offset 까지의 범위를 삭제한다. 
- 중간의 특정 데이터만 삭제할 수는 없음
```
# partition 0번의 offset 0~2 까지의 데이터를 삭제한다. 
> bin/kafka-delete-records.sh --bootstrap-server localhost:9092 --offset-json-file ./delete-offset.json
Executing records delete operation
Records delete operation completed:
partition: kv_topic-0	low_watermark: 2


> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic --from-beginning
## msg3, msg4 데이터가 삭제됨
msg1
msg2
msg5
msg6
```

#### delete_offset.json
```json
{
    "partitions": [
    {"topic": "kv_topic", "partition":0, "offset": 2}
    ], 
    "version":1
}
```


## 2. 운영관련 Command 
### Dump kafka log file(segment)
```
> bin/kafka-dump-log.sh --print-data-log --files /tmp/kafka-logs/kv_topic-0/00000000000000000000.log

Dumping /tmp/kafka-logs/kv_topic-0/00000000000000000000.log
Starting offset: 0   <-- offset 시작점

## offset 0 번째 데이터 정보 출력  
baseOffset: 0 lastOffset: 0 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 0 CreateTime: 1648305071780 size: 74 magic: 2 compresscodec: none crc: 585719343 isvalid: true
| offset: 0 CreateTime: 1648305071780 keySize: 2 valueSize: 4 sequence: -1 headerKeys: [] key: k3 payload: msg3

## offset 1 번째 데이터 출력  
baseOffset: 1 lastOffset: 1 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 74 CreateTime: 1648305075366 size: 74 magic: 2 compresscodec: none crc: 1275813315 isvalid: true
| offset: 1 CreateTime: 1648305075366 keySize: 2 valueSize: 4 sequence: -1 headerKeys: [] key: k4 payload: msg4
baseOffset: 2 lastOffset: 2 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 148 CreateTime: 1648305078891 size: 74 magic: 2 compresscodec: none crc: 545986219 isvalid: true
| offset: 2 CreateTime: 1648305078891 keySize: 2 valueSize: 4 sequence: -1 headerKeys: [] key: k5 payload: msg5
baseOffset: 3 lastOffset: 3 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 222 CreateTime: 1648308346400 size: 74 magic: 2 compresscodec: none crc: 610339906 isvalid: true
| offset: 3 CreateTime: 1648308346400 keySize: 2 valueSize: 4 sequence: -1 headerKeys: [] key: k7 payload: msg7
```

### Topic의 partition 별로 마지막 commit 된 위치 확인
```
> cat /tmp/kafka-logs/replication-offset-checkpoint
kv_topic 0 4  <-- partition 0은 마지막 commit offset이 4
kv_topic 1 3
```

#### 다시 데이터를 전송한 후, commit 값이 증가했는지 확인 
```
> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic kv_topic \
> --property "parse.key=true" \
> --property "key.separator=:" \
> --property "print.key=true"
>k8:msg8
>k9:msg9

> cat /tmp/kafka-logs/replication-offset-checkpoint
kv_topic 0 6 <-- partition 0에만 위 2건이 추가된 commit 확인 가능
kv_topic 1 3
``` 

## 현재 Broker 설정 확인 
```
> bin/kafka-configs.sh --bootstrap-server localhost:9092 --broker 0 --describe --all
All configs for broker 0 are:
  log.cleaner.min.compaction.lag.ms=0 sensitive=false synonyms={DEFAULT_CONFIG:log.cleaner.min.compaction.lag.ms=0}
  offsets.topic.num.partitions=50 sensitive=false synonyms={DEFAULT_CONFIG:offsets.topic.num.partitions=50}
  log.flush.interval.messages=9223372036854775807 sensitive=false synonyms={DEFAULT_CONFIG:log.flush.interval.messages=9223372036854775807}
  controller.socket.timeout.ms=30000 sensitive=false synonyms={DEFAULT_CONFIG:controller.socket.timeout.ms=30000}
  log.flush.interval.ms=null sensitive=false synonyms={}
  principal.builder.class=org.apache.kafka.common.security.authenticator.DefaultKafkaPrincipalBuilder sensitive=false synonyms={DEFAULT_CONFIG:principal.builder.class=org.apache.kafka.common.security.authenticator.DefaultKafkaPrincipalBuilder}
  controller.quorum.request.timeout.ms=2000 sensitive=false synonyms={DEFAULT_CONFIG:controller.quorum.request.timeout.ms=2000}
  min.insync.replicas=1 sensitive=false synonyms={DEFAULT_CONFIG:min.insync.replicas=1}
  num.recovery.threads.per.data.dir=1 sensitive=false synonyms={STATIC_BROKER_CONFIG:num.recovery.threads.per.data.dir=1, DEFAULT_CONFIG:num.recovery.threads.per.data.dir=1}
.....
```

### topic의 모든 데이터를 삭제 
- 삭제하기 이전의 sement 파일 확인 
```
> ls /tmp/kafka-logs/kv_topic-0
00000000000000000000.index  00000000000000000000.log  00000000000000000000.timeindex  00000000000000000003.snapshot  leader-epoch-checkpoint  partition.metadata

> ls /tmp/kafka-logs/kv_topic-1
00000000000000000000.index  00000000000000000000.log  00000000000000000000.timeindex  00000000000000000002.snapshot  leader-epoch-checkpoint  partition.metadata
```

- kv_topic 데이터 삭제 
    - 직접 삭제하는 것이 아니라, 데이터를 보유하는 기간을 0으로 조정하여, 
    - 그 이전 데이터는 broker가 자동으로 삭제
```
> bin/kafka-configs.sh --bootstrap-server localhost:9092 --topic kv_topic --add-config retention.ms=0 --alter
Completed updating config for topic kv_topic.
```

- 약 5분 정도 후에 다시 segment 파일을 조회하면 기존 segment 파일(00000.log)은 삭제되고
- partition 0는 6.log 파일이 새롭게 생성되고, 
- partition 1은 3.log 파일이 새롭게 생성되었다. 

```
> /tmp/kafka-logs/kv_topic-0
00000000000000000000.index.deleted  00000000000000000000.timeindex.deleted  00000000000000000006.log       leader-epoch-checkpoint
00000000000000000000.log.deleted    00000000000000000003.snapshot           00000000000000000006.snapshot  partition.metadata

> ls /tmp/kafka-logs/kv_topic-1
00000000000000000000.index.deleted  00000000000000000000.timeindex.deleted  00000000000000000003.log       leader-epoch-checkpoint
00000000000000000000.log.deleted    00000000000000000002.snapshot           00000000000000000003.snapshot  partition.metadata
```

- 변경했던 옵션을 삭제
```
> bin/kafka-configs.sh --bootstrap-server localhost:9092 --topic kv_topic --delete-config retention.ms --alter
Completed updating config for topic kv_topic.

## Config에 retention.ms 옵션이 삭제됨
> bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic kv_topic --describe
Topic: kv_topic	TopicId: JuKdf41ASVKbZXEKru3iLA	PartitionCount: 2	ReplicationFactor: 1	Configs: segment.bytes=1073741824
	Topic: kv_topic	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
	Topic: kv_topic	Partition: 1	Leader: 0	Replicas: 0	Isr: 0
```


## 관련 github repository

- https://github.com/onlybooks/kafka2 실전 카프카 개발부터 운영까지

- https://github.com/bjpublic/apache-kafka-with-java 아파치 카프카 애플리케이션 프로그래밍 with 자바

- https://github.com/bstashchuk/apache-kafka-course The Complete Apache Kafka Practical Guide

### Fastcampus kafka 강의 자료
- https://github.com/jingene/fastcampus_kafka_handson Part 2. 실무에서 쉽게 써보는 Kafka

- https://github.com/fast-campus-lecture Part 3. Spring for Apache Kafka

- https://github.com/freepsw/kafka-metrics-monitoring Part 4. 실시간 모니터링을 위한 Kafka 매트릭 이해