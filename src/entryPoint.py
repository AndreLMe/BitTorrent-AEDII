import sys
import json
from peer import Peer

paramsString = sys.argv[1]
paramsDict = json.loads(paramsString)

if paramsDict["nodeType"] == "peer":
    peers = []
    for peer in paramsDict["knownPeers"]:
        peers.append({"addr": (peer["ip"], peer["port"]), "maxIdHash": peer["maxIdHash"]})
    peer = Peer((paramsDict["ip"], paramsDict["port"]),\
                peers, int(paramsDict["maxIdHash"], base=16), peers[0], peers[2])