import streamlit as st
import pika
credentials = pika.PlainCredentials('username', 'password')
connection =pika.BlockingConnection(pika.ConnectionParameters('192.168.0.122',port=5672, virtual_host='/',credentials=credentials))
channel=connection.channel()
channel.queue_declare(queue='TEMP_PRESSURE',durable=True)
st.title("TEMP_PRESSURE")
message_placeholder = st.empty()
def callback(ch,method,body,properties):
    st.write(f"Recived message:{body.decode()}")
    channel.basic_consume(queue='TEMP_PRESSURE',on_message_callback=callback,auto_ack=True)
if st.button("start Listening"):
    st.write("Listening for messages")
    channel.start_consuming()