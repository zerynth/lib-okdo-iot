# -*- coding: utf-8 -*-

"""
.. module:: iot

****************
OKdo IoT Library
****************

The Zerynth OKdo IoT Library can be used to ease the connection to the `OKdo IoT Cloud <https://www.okdo.com/us/do-iot/>`_.

It makes your device act as an OKdo IoT Device which can be created and provisioned on the OKdo IoT Cloud dashboard.

The device always send and receive data in the JSON format.

Check out the examples for a jump start.

    """

class Device():
    """
================
The Device class
================

.. class:: Device(device_id, device_token, client)

        Create a Device instance representing an OKdo device.

        The device is provisioned by the :samp:`device_id` and :samp:`device_token`, obtained from the OKdo dashboard upon the creation of a new device.
        the :samp:`client` parameter is a class that provides the implementation of the low level details for the connection. It can be one of :samp:`MqttClient` in the :samp:`mqtt_client` module, or :samp:`HttpClient` in the :samp:`http_client` module.


    """
    def __init__(self,device_id, device_token, client,endpoint="api.allthingstalk.io"):
        self.client = client(endpoint,device_id,device_token)
        self.assets = {}


    def connect(self):
        """
.. method:: connect()
    
        Setup a connection to the OKdo Cloud. It can raise an exception in case of error.

        """
        self.client.connect()

    def run(self):
        """
.. method:: run()
    
        Starts the device by executing the underlying client. It can start a new thread depending on the type of client (Mqtt vs Http)

        """
        self.client.loop()

    def publish_asset(self,asset_name,value):
        """
.. method:: publish_asset(asset_name,value)
        
        Modify a device asset state. After a successful execution, the new state of the device asset :samp:`asset_name` will be set to :samp:`value`.

        Return the message sent to the OKdo Cloud, or :samp:`None` if the message cannot be sent.
        """

        return self.client.publish_asset(asset_name,value)

    def publish_state(self,state):
        """
.. method:: publish_state(state)
        
        Modify a device state. After a successful execution, the new state of the device will be set to the values contained in :samp:`state`. :samp:`state` is
        a dict where each key is the name of an asset and each value the desired state.

        Return the message sent to the OKdo Cloud, or :samp:`None` if the message cannot be sent.
        """
        return self.client.publish_state(state)


    def watch_command(self,asset_name,callback):
        """
.. method:: watch_command(asset_name, callback)
       
        Start listening for asset command on the device asset identified by :samp:`asset_name`. When a new asset command arrives, the function :samp:`callback` is executed receiving as arguments the asset name, the new value and the previous value (or None if it is the first update).
        Incoming values are checked against the last received timestamp in order to avoid triggering the callback for 
        Modify a device state. After a successful execution, the new state of the device will be set to the values contained in :samp:`state`. :samp:`state` is
        a dict where each key is the name of an asset and each value the desired state.

        Return the message sent to the OKdo Cloud, or :samp:`None` if the message cannot be sent.
        """
        if asset_name not in self.assets:
            self.assets[asset_name] = {"ts":"0","value":None}
        self.assets[asset_name]["cb"]=callback
        self.client.on_command(asset_name,self.command_incoming)

    def command_incoming(self,asset_name,msg):
        try:
            asset = self.assets[asset_name]
            pts = asset["ts"]
            pv = asset["value"]
            # print("Less",pts<msg["at"],pts,msg["at"])
            #TODO: fix vm bug
            #if pts<msg["at"]:
            # it's a new update!
            asset["ts"]=msg["at"]
            asset["value"]=msg["value"]
            if asset["cb"]:
                asset["cb"](asset_name,msg["value"],pv)
        except Exception as e:
            print(e)





