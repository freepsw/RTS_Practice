from confluent_kafka import Producer
from random import choice

p = Producer({'bootstrap.servers': 'localhost'})

# Call back function (어떤 partition에 할당 되었는지 확인)
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Producer가 데이터를 전송한 후 callback 함수가 호출되기까지 대기하는 시간
user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']

for _ in range(10):
    p.poll(0)
    user_id = choice(user_ids)
    product = choice(products)
    p.produce('my_topic', product, user_id, callback=delivery_report)

p.flush()