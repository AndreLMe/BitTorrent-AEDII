import sys
import json
from peer import Peer
from main import Client
from serverInfo import ServerInfo

paramsString = sys.argv[1]
paramsDict = json.loads(paramsString)
print("TESSTTTTT")

if paramsDict["nodeType"] == "peer":
    peers = []
    for peer in paramsDict["knownPeers"]:
        peers.append(ServerInfo((peer["ip"], peer["port"]), int(peer["maxIdHash"], base=16)))

    print("Entrando no peer")
    suc = paramsDict["sucessor"]
    pred = paramsDict["predecessor"]

    peer = Peer((paramsDict["ip"], paramsDict["port"]),\
                peers, int(paramsDict["maxIdHash"], base=16),\
                ServerInfo((suc["ip"], suc["port"]), int(suc["maxIdHash"], 16)), ServerInfo((pred["ip"], pred["port"]), int(pred["maxIdHash"], 16)))
    
if paramsDict["nodeType"] == "client":
    client = Client(paramsDict["ip"], paramsDict["port"])