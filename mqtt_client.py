from mqtt import mqtt
import json


class MqttClient():
    def __init__(self,endpoint,device_id,device_token):
        self.uid = device_id
        self.token = device_token
        self.endpoint = endpoint
        self.type = "mqtt"
        self.driver = mqtt.Client(device_id,False)
        self.driver.set_username_pw(device_token,"okdo")
        self.command_callbacks = {}


    def connect(self):
        for retry in range(10):
            try:
                self.driver.connect(self.endpoint, 60)
                break
            except Exception as e:
                sleep(1000)
        else:
            self.driver.connect(self.endpoint, 60)

    def loop(self):
        self.driver.loop(self._on_msg)

    def _on_msg(self,client,data):
        msg = data["message"]
        asset = self.get_asset_from_url(msg.topic)
        if asset in self.command_callbacks and self.command_callbacks[asset]:
            self.command_callbacks[asset](asset,json.loads(msg.payload))

    def get_asset_from_url(self,url):
        # url of format xxxxx/asset/<asset_name>/type
        fields = url.split("/")
        return fields[-2]

    def asset_url(self,asset,type):
       return "device/"+self.uid+"/asset/"+asset+"/"+type

    def state_url(self):
       return "device/"+self.uid+"/state"

    def publish_asset(self, asset, value):
        obj = {"value":value}
        self.driver.publish(self.asset_url(asset,"state"), json.dumps(obj))
        return obj

    def publish_state(self, state):
        obj = {}
        for k,v in state.items():
            obj[k]={"value":v}
        self.driver.publish(self.state_url(), json.dumps(obj))
        return obj

    def on_command(self,asset,callback,qos=1):
        topic = self.asset_url("+","command")
        self.driver.subscribe([[topic,qos]])
        self.command_callbacks[asset]=callback


