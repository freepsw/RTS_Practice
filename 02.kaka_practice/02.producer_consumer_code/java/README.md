# Apache Kafka Producer & Consumer 구현 (Java)
- https://developer.confluent.io/tutorials/kafka-producer-callback-application/confluent.html

## Download java project
```
> sudo yum install -y git maven

> cd ~
> git clone https://github.com/freepsw/RTS_Practice
> cd RTS_Practice/02.kaka_practice/02.producer_consumer_code/java/
> cd my-kafka-java/
```

## Compile and Run Java Producer & Consumer 
### Compile java 
```
> mvn clean package
```

## Run kafka console consumer & producer 
```
> cd $KAFKA_HOME
> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic my_topic


> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kv_topic --from-beginning

> bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic kv_topic \
--property "parse.key=true" \
--property "key.separator=:" \
--property "print.key=true"
k1:msg1

```

## Run Producer and Consumer 
### Run Producer 
```
> mvn exec:java -Dexec.mainClass="Producer_Sync"
ProducerRecord(topic=my_topic, partition=null, headers=RecordHeaders(headers = [], isReadOnly = true), key=null, value=simple producer message, timestamp=null)


> mvn exec:java -Dexec.mainClass="Producer_Callback_Sync"
Record written to offset 25 timestamp 1648373316114

> mvn exec:java -Dexec.mainClass="Producer_Callback_Async"
Record written to offset 28 timestamp 1648373544238

```

### Run Consumer 
```
> mvn exec:java -Dexec.mainClass="Consumer_Simple"

ConsumerRecord(topic = my_topic, partition = 1, leaderEpoch = 0, offset = 25, CreateTime = 1648373795837, serialized key size = 7, serialized value size = 9, headers = RecordHeaders(headers = [], isReadOnly = false), key = sgarcia, value = gift card)

> mvn exec:java -Dexec.mainClass="Consumer_Commit_Auto"

ConsumerRecord(topic = my_topic, partition = 0, leaderEpoch = 0, offset = 32, CreateTime = 1648373867522, serialized key size = 8, serialized value size = 9, headers = RecordHeaders(headers = [], isReadOnly = false), key = jbernard, value = batteries)


> mvn exec:java -Dexec.mainClass="Consumer_Commit_Sync"

ConsumerRecord(topic = my_topic, partition = 0, leaderEpoch = 0, offset = 46, CreateTime = 1648373922585, serialized key size = 8, serialized value size = 9, headers = RecordHeaders(headers = [], isReadOnly = false), key = jbernard, value = batteries)"


> mvn exec:java -Dexec.mainClass="Consumer_Commit_Async"

ConsumerRecord(topic = my_topic, partition = 0, leaderEpoch = 0, offset = 52, CreateTime = 1648374010211, serialized key size = 6, serialized value size = 9, headers = RecordHeaders(headers = [], isReadOnly = false), key = eabara, value = batteries)
Commit succeeded
```


## ETC 
### Java project using maven
- https://kafka.apache.org/25/javadoc/overview-summary.html

### Java project using gradle
- https://developer.confluent.io/tutorials/kafka-producer-callback-application/confluent.html#initialize-the-project