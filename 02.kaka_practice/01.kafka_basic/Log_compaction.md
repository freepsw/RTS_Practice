# Log Cleansing 

## Delete Log Examples
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

## Log Compaction Examples 

```
kafka-topics --create --zookeeper zookeeper:2181 --topic latest-product-price --replication-factor 1 --partitions 1 --config "cleanup.policy=compact" --config "delete.retention.ms=100"  --config "segment.ms=100" --config "min.cleanable.dirty.ratio=0.01"

> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic log_compact_topic \
  --config "cleanup.policy=compact" \
  --config "delete.retention.ms=100"  \
  --config "segment.ms=100" \
  --config "min.cleanable.dirty.ratio=0.01"

> bin/kafka-topics.sh --list --bootstrap-server localhost:9092

## Produce key-value message 
> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic log_compact_topic \
--property "parse.key=true" \
--property "key.separator=:" \
--property "print.key=true"
k1:msg11
k2:msg21
k3:msg31
k1:msg12
k2:msg22
k3:msg32
k1:msg13
k2:msg23


## 약 5분 정도 후에 아래 consumer를 통해서 메세지를 확인해 본다. 
## 5분은 내부적으로 broker의 log cleaner가 동작하는 시간 고려
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic log_compact_topic \
--property print.key=true \
--property key.separator=":" \
--from-beginning
k2:msg22
k3:msg32
k1:msg13
k2:msg23 <-- 아마도 이 메시지는 active segment에 있기 때문에 중복 제거가 되지 않았을 듯
```