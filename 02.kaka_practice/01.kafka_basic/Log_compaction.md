# Log Compaction Examples 

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