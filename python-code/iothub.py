import iothub_client
from iothub_client import *
from time import sleep
import json

timeout = 241000
minimum_polling_time = 9
receive_context = 0
connection_string = 'Device Connection String'

def receive_message(message, counter):
  buffer = message.get_bytearray()
  size = len(buffer)
  message = json.loads(buffer[:size].decode('utf-8')).get('message')
  print("Received Data: <%s>" % message)
  return IoTHubMessageDispositionResult.ACCEPTED

def iothub_init():
  iotHubClient = IoTHubClient(connection_string, IoTHubTransportProvider.HTTP)
  iotHubClient.set_option("timeout", timeout)
  iotHubClient.set_option("MinimumPollingTime", minimum_polling_time)
  iotHubClient.set_message_callback(receive_message, receive_context)
  while True:
    sleep(10)

if __name__ == '__main__':
  iotHubClient = iothub_init()
