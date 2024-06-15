import pika
import json
import mysql.connector


# Establish RabbitMQ connection
def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="test_queue")
    message = {"id": 8, "name": "abc", "value": 1.5}
    channel.basic_publish(
        exchange="",
        routing_key="test_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )
    return connection, channel


# Establish MySQL connection
def connect_mysql():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0944424190",
        database="rabbitmq",
    )
    cursor = connection.cursor()
    return connection, cursor


# Insert data into MySQL table
def insert_data(cursor, connection, data):
    sql = "INSERT INTO data_table (id, name, value) VALUES (%s, %s, %s)"
    val = (data["id"], data["name"], data["value"])
    cursor.execute(sql, val)
    connection.commit()


# Process data received from the queue
def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received {data}")

    try:
        connection, cursor = connect_mysql()
        insert_data(cursor, connection, data)
        cursor.close()
        connection.close()
        print("Data inserted into MySQL")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Listen to the queue and process the data
def main():
    connection, channel = connect_rabbitmq()
    channel.basic_consume(
        queue="test_queue", on_message_callback=callback, auto_ack=True
    )
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
    connection.close()


if __name__ == "__main__":
    main()
