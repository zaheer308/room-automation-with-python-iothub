import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult, IoTHubError, DeviceMethodReturnValue
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.cleanup(5)

GPIO.setup(5, GPIO.OUT)

WAIT_COUNT = 5
METHOD_CONTEXT = 0
METHOD_CALLBACKS = 0

# chose MQTT or MQTT_WS as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
CONNECTION_STRING = "Device Connection String"

def device_method_callback(method_name, payload, user_context):
    global METHOD_CALLBACKS

    if method_name == "DeviceMethod":
        onDeviceMethod()

    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s\ncontext = %s" % (method_name, payload, user_context) )
    METHOD_CALLBACKS += 1


    loaditnow = payload
    clienton = '{"ClickButton":"ON1"}'
    clientoff = '{"ClickButton":"OFF1"}'

    print ( "\npayload should show now= %s \nclienton = %s\nclientoff = %s" % ( loaditnow, clienton, clientoff) )

    
    if loaditnow == clienton:
        GPIO.output(5, True)
    elif loaditnow == clientoff:
        GPIO.output(5, False)

    print ( "Total calls confirmed: %d\n" % METHOD_CALLBACKS )
    device_method_return_value = DeviceMethodReturnValue()
    device_method_return_value.response = "{ \"Response\": \"Operation was successful\" }"
    device_method_return_value.status = 200

    return device_method_return_value

def onDeviceMethod():
    print ( "Direct method called." )

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)

    if client.protocol == IoTHubTransportProvider.MQTT or client.protocol == IoTHubTransportProvider.MQTT_WS:
        client.set_device_method_callback(device_method_callback, METHOD_CONTEXT)

    return client

def iothub_client_sample_run():
    try:
        client = iothub_client_init()

        while True:
            print ( "IoTHubClient waiting for direct method call, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                time.sleep(10)
                status_counter += 1
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "Starting the IoT Hub Python direct methods sample..." )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_client_sample_run()

    
