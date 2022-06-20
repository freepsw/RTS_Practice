# Apache Kafka Connect

## Simple Tutorial 
- https://kafka.apache.org/quickstart
### STEP 1. Config Kafka Connect 
- Kafka Connect에서 사용할 library를 추가한다. 
```
> cd #KAFKA_HOME 
> vi config/connect-standalone.properties

# 아래 항목 추가 
plugin.path=lib/connect-file-3.2.0.jar
```

#### STEP 2. Create a file for testing 
```
> cd $KAFKA_HOME
> echo -e "foo\nbar" > test.txt
```

### STEP 3. Create the config file for source and sink 
#### Source properties 
```
> cd $KAFKA_HOME 
> vi config/connect-file-source.properties
```
- connect-file-source.properties
```properties
name=local-file-source
connector.class=FileStreamSource
tasks.max=1
file=test.txt
topic=connect-test
```

#### Sink properties 
```
> cd $KAFKA_HOME 
> vi config/connect-file-sink.properties
```



### STEP 4. Run the kafka connect server 
```
> bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties
```

### STEP 5. Read the kafka topic using console_consumer 
```
> cd $KAFKA_HOME
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning
{"schema":{"type":"string","optional":false},"payload":"foo"}
{"schema":{"type":"string","optional":false},"payload":"bar"}
```

