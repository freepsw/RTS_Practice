from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from elasticsearch import Elasticsearch
from datetime import datetime

value_schema_str = """
{"namespace": "student.avro",
 "type": "record",
 "doc": "This is an example of Avro.",
 "name": "Student",
 "fields": [
     {"name": "name", "type": ["null", "string"], "default": null, "doc": "Name of the student"},
     {"name": "class", "type": "int", "default": 1, "doc": "Class of the student"}
 ]
}
"""

value_schema = avro.loads(value_schema_str)

c = AvroConsumer({
    'bootstrap.servers': 'peter-zk01.foo.bar,peter-zk02.foo.bar,peter-zk03.foo.bar',
    'group.id': 'python-groupid01',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': 'http://peter-kafka03.foo.bar:8081'},reader_value_schema=value_schema)

c.subscribe(['src.peter-avro01-kafka1'])

es = Elasticsearch('peter-kafka02.foo.bar:9200')
index = 'students'

while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value())
    doc = msg.value()
    doc['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
#    doc['timestamp'] = datetime.now()

    if not es.indices.exists(index=index):
        es.indices.create(index=index)
    es.index(index=index, doc_type='_doc', body=doc)

c.close()