import requests


class HttpClient():
    def __init__(self,endpoint,device_id,device_token):
        self.uid = device_id
        self.token = device_token
        self.endpoint = "http://"+endpoint+"/"
        self.type = "http"
        self.headers = {
            "Authorization":"Bearer "+self.token,
            "Content-Type":"application/json"
        }


    def connect(self):
        pass

    def loop(self):
        pass


    def asset_url(self,asset,type):
        return self.endpoint+"device/"+self.uid+"/asset/"+asset+"/"+type

    def state_url(self):
        return self.endpoint+"device/"+self.uid+"/state"

    def publish_asset(self, asset, value):
        obj = {"value":value}
        try:
            res = requests.put(self.asset_url(asset,"state"),json=obj,headers=self.headers)
        except Exception as e:
            return None
        if res.status!=200:
            return None
        return obj

    def publish_state(self, state):
        obj = {}
        for k,v in state.items():
            obj[k]={"value":v}
        try:
            res = requests.put(self.state_url(),json=obj,headers=self.headers)
        except Exception as e:
            return None
        if res.status!=204:
            return None
        return obj

    def on_command(self,asset,callback,qos=1):
        pass


