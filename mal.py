import requests


class BlockchainMaster(object):
    """docstring forBeyfendi."""

    def __init__(self):
        self.nodes = []


    def registerNode(self, address, nodes):
        resp = requests.post(address, data={"nodes": nodes})
        if resp.status_code == 201:
            return(resp.json())
    def consensus(self):
        pass

class Beyfendi(object):
    """docstring forBeyfendi."""

    def __init__(self, ad, node):
        self.ad = ad
        self.node = node
        self.coin = 0
    def mine(self):
        resp = requests.get(self.node+"/mine")
        if resp.status_code == 200:
            for transaction in resp.json()["transactions"]:
                self.coin += transaction['amount']
