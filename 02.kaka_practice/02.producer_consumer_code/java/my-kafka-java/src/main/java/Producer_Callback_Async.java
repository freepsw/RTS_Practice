import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

public class Producer_Callback_Async {
    public static void main(String[] args) {
        Properties configs = new Properties();
        configs.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        configs.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        configs.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        KafkaProducer<String, String> producer = new KafkaProducer<>(configs);

        String msg = "Async producer message";
        ProducerRecord<String, String> record = new ProducerRecord<>("my_topic", msg);
        producer.send(record, (recordMetadata, exception) -> {
            if (exception == null) {
                System.out.println("Record written to offset " +
                        recordMetadata.offset() + " timestamp " +
                        recordMetadata.timestamp());
            } else {
                System.err.println("An error occurred");
                exception.printStackTrace(System.err);
            }
        });
        producer.flush();
        producer.close();
    }
}
