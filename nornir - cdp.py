

from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os
import sys
import json
import yaml
import NextUI_Func

nr = InitNornir(config_file="config.yaml")

nor_HOSTNAME = nr.run(netmiko_send_command, command_string = 'show run | in hostname', use_textfsm=True)
nor_CDP_DET = nr.run(netmiko_send_command, command_string = 'show cdp neighbors detail', use_textfsm=True)
nor_VERSION = nr.run(netmiko_send_command, command_string = 'show version', use_textfsm=True)
topologia = NextUI_Func.topologyData()

for device in nor_HOSTNAME.keys():
    if device not in nor_HOSTNAME.failed_hosts.keys():
        print(device, nor_VERSION[device][0].result[0]['hostname'])
        equipo = NextUI_Func.Devices(device, nor_VERSION[device][0].result[0]['hostname'])
        equipo.encode_password(nor_VERSION[device][0].result[0]['hostname'])
        
        equipo.set_version(nor_VERSION[device][0].result)
        equipo.set_cdp_neighbors_table(nor_CDP_DET[device][0].result)
        equipo.set_icon(nor_VERSION[device][0].result)
        
        topologia.add_nodes(equipo.df_nodes)
        topologia.add_links(equipo.df_links)

topologia.add_js()
topologia.depurar_links()
topologia.to_file('NextUI-CDP/topology.js')
