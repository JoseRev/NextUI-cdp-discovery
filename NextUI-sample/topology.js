var topologyData = {
  "nodes": [
    {
      "index": 0,
      "name": "R1",
      "hostname": "10.0.0.1",
      "username": "cisco",
      "password": "cisco",
      "encoded_password": "Y2lzY28=",
      "tipo": "inventario",
      "connection": "cisco_ios_telnet",
      "serial": "FHK1438F0C1",
      "model": "CISCO2911/K9",
      "icon": "router",
      "id": 0
    },
    {
      "index": 0,
      "name": "SW1",
      "hostname": "10.0.0.3",
      "username": "cisco",
      "password": "cisco",
      "encoded_password": "Y2lzY28=",
      "tipo": "inventario",
      "connection": "cisco_ios_telnet",
      "serial": "FOC1737Z351",
      "model": "WS-C2960S-48LPS-L",
      "icon": "switch",
      "id": 1
    },
    {
      "index": 0,
      "name": "24b6570ca6ab",
      "hostname": "192.168.1.254",
      "username": NaN,
      "password": NaN,
      "encoded_password": NaN,
      "tipo": "cdp",
      "connection": NaN,
      "serial": "linux - Debian",
      "model": "SF200-24(PID:SLM224GT)-VSD",
      "icon": "server",
      "id": 2
    }
  ],
  "links": [
    {
      "id": 0,
      "source": 0,
      "srcDevice": "R1",
      "srcIfName": "Gi0/1",
      "target": 1,
      "tgtDevice": "SW1",
      "tgtIfName": "Gi1/0/38"
    },
    {
      "id": 1,
      "source": 1,
      "srcDevice": "SW1",
      "srcIfName": "Gi1/0/28",
      "target": 2,
      "tgtDevice": "24b6570ca6ab",
      "tgtIfName": "fa21"
    }
  ],
  "nodeSet": []
}