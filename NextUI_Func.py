import pandas as pd
import ipaddress
import json
import base64
import yaml
import os
import ipaddress
import datetime

# NextUI.py define:
# Las Clases Devices y topologyData (serviran para generar una la topologia por CDP)


class Devices:
    def __init__(self, inventory_name, cli_name):
        self.cli_name = cli_name
        self.inventory_name = inventory_name
        self.df_nodes = pd.DataFrame()
        self.df_links = pd.DataFrame()

    def encode_password(self, name_cli ):
        """
        - Inicializa dataframe df_nodes, con el nombre del host de hosts.yaml (columna name)
        - Busca la IP del dispositivo, y la agrega a df_nodes (columna hostname)
        - Busca password del dispotivo, y la agrega (columna password)
        - Codfica el password del dispositivo y la agrega (columna encoded_password)
        - df_nodes =
            encoded_password         hostname                    name    password
            QzNDME1SM0QzNQ==    10.201.209.15           SWCORE_CECOM2  C3C0MR3D35
        """
        path='inventory/hosts.yaml'
        device_name = self.inventory_name
        
        # Abrir hosts.yaml
        with open(path) as file:
             hosts = yaml.load(file, Loader=yaml.FullLoader)

        # Encode base64 password
        password = hosts[device_name].get('password')
        sample_string = password
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        self.df_nodes= self.df_nodes.append({
                        'name': name_cli,
                        'hostname': hosts[device_name].get('hostname'),
                        'username': hosts[device_name].get('username'),
                        'password': password,
                        'encoded_password': base64_string,
                        'tipo':'inventario',
                        'connection': hosts[device_name].get('platform')
                        },ignore_index=True)


    # Nornir info
    def set_version(self, version_textfsm):
        """
        - Agrega informacion de serie y hardware al dispositivo
        """
        self.df_nodes['serial'] = version_textfsm[0]['serial'][0]
        self.df_nodes['model']  = version_textfsm[0]['hardware'][0]

    def set_connection(self):
        """
        - SSH/Telnet
        """
        self.df_nodes.loc[self.df_nodes['connection']=="cisco_ios", 'connection']='ssh'
        self.df_nodes.loc[self.df_nodes['connection']=="cisco_ios_telnet", 'connection']='telnet'
        self.df_nodes.loc[self.df_nodes['connection']=="cisco_s300", 'connection']='ssh'

    def set_vlans(self, sh_interface, vlan_brief):
        """
        - Definir en DataFrame las vlans de los hosts remotos.
        - Utiliza el resultado de los comandos: 'show vlan brief'
        (Pdb++) df_vlan.loc[:,['interface', 'mode','access_vlan']]
           interface           mode access_vlan 
        0    Gi1/0/1           down           1
        27  Gi1/0/28          trunk           2
        37  Gi1/0/38  static access           1
        
        (Pdb++) df_vlan
        vlan_id                name     status                                         interfaces
        0       1             default     active  [Gi1/0/1, Gi1/0/2, Gi1/0/3, Gi1/0/4, Gi1/0/5, ...
        1       2                 jid     active                                         [Gi1/0/24]
        """
        df_bkp=self.df_nodes
        try:
            df_sw=pd.DataFrame(sh_interface)
            df_sw=df_sw.loc[:,['interface', 'mode','access_vlan']]
            filt = df_sw['mode'] != 'down'
            df_sw.loc[filt]
            df_vlan = pd.DataFrame(vlan_brief).loc[:,['vlan_id','name']]
            
            df=pd.merge(df_sw, df_vlan, how='right', left_on='access_vlan', right_on='vlan_id')
            #df=pd.merge(df_sw,df_vlan, on = [;;]how='outer')
        except:
            self.df_nodes = df_bkp
                    
    def set_vlan_interface(self, core_ip_interface, core_vlan_brief):
        """
        - Definir en DataFrame las vlans de los hosts remotos.
        - Utiliza el resultado de los comandos: 'show ip interface', 'show vlan brief'        
        """
        df_bkp=self.df_nodes
        try:
            df_vlan=pd.DataFrame(core_vlan_brief)
            df_vlan['vlan']=df_vlan['vlan_id']
            df_vlan=df_vlan.loc[:,['vlan', 'name']] ## 'interfaces'???

            df_ip=pd.DataFrame(core_ip_interface)
            df_ip=df_ip.loc[df_ip['intf'].str.match("Vlan"),['intf', 'ipaddr','mask']]
            df_ip=df_ip.replace(to_replace='Vlan', value='', regex=True)
            df_ip['ipaddr']= df_ip['ipaddr'].apply(lambda x: x+['0.0.0.0'])
            df_ip['ipaddr']= df_ip['ipaddr'].apply(lambda x: x[0])
            df_ip['mask']= df_ip['mask'].apply(lambda x: x+['32'])
            df_ip['mask']= df_ip['mask'].apply(lambda x: x[0])
            for row in df_ip.index:
                df_ip.loc[row, 'interface']=ipaddress.ip_interface(df_ip.loc[row, 'ipaddr']+'/'+df_ip.loc[row,'mask'])
            df_ip["vlan"]=df_ip["intf"]
            df_ip=df_ip.loc[:,['vlan', 'interface']]

            df=pd.merge(df_ip,df_vlan, how='outer')
            self.df_nodes['vlan']=''
            self.df_nodes.reset_index(drop=True, inplace=True)
            for row_host in self.df_nodes.index:
                try:
                    ip=ipaddress.ip_address(self.df_nodes.loc[row_host,'hostname'])
                    for row_core in df.index:
                        interface=df.loc[row_core,'interface']
                        try:
                            if ip in df.loc[row_core,'interface'].network:
                                self.df_nodes.loc[row_host,'vlan']=df.loc[row_core,'vlan']+', '+df.loc[row_core,'name']
                        except:
                            pass
                except:
                    pass
        except:
            self.df_nodes = df_bkp
            
    def set_icon(self, version_textfsm):
        """
        - Pone el icono al dataframe (df_nodes)
        """
        icon = version_textfsm[0]['serial'][0]
        df = self.df_nodes
        df['icon'] = ''
        df.loc[df['model'].str.match('Phone'),"icon"]='ipphone'
        df.loc[df['model'].str.match('IPPhone'),"icon"]='ipphone'
        df.loc[df['model'].str.match('SIP'),"icon"]='ipphone'
        df.loc[df['model'].str.match('SEP'),"icon"]='ipphone'
        df.loc[df['model'].str.match('T23G'),"icon"]='ipphone'
        df.loc[df['model'].str.match('T41S'),"icon"]='ipphone'
        df.loc[df['model'].str.match('T29'),"icon"]='ipphone'
        df.loc[df['model'].str.match('GXP'),"icon"]='ipphone'
        df.loc[df['model'].str.match('VMware'),"icon"]='server'
        df.loc[df['model'].str.match('ESX'),"icon"]='server'
        df.loc[df['model'].str.match('Elastix'),"icon"]='server'
        df.loc[df['model'].str.match('SF'),"icon"]='switch'
        df.loc[df['model'].str.match('SG'),"icon"]='switch'
        df.loc[df['model'].str.match('N3K'),"icon"]='switch'
        df.loc[df['model'].str.match('WS-'),"icon"]='switch'
        df.loc[df['model'].str.match('CISCO', case=False),"icon"]='router'
        df.loc[df['model'].str.match('1811'),"icon"]='router'
        df.loc[df['model'].str.match('1900'),"icon"]='router'
        df.loc[df['model'].str.match('2811'),"icon"]='router'
        df.loc[df['model'].str.match('3845'),"icon"]='router'
        df.loc[df['model'].str.match('3825'),"icon"]='router'
        df.loc[df['model']=='',"icon"]='host'
        self.df_nodes = df

    def set_cdp_neighbors_table(self, cdp_table_textfsm):
        """
        - Por ciclo de nornir[device][0].results, Crea un dataframe con los datos de "cdp neighbors"
        - Merge con df_nodes, (DataFrame de todos los nodos)
        -------------------------------------------------------------------------------------------------------------
            - df_nodes =
                encoded_password         hostname                    name    password       serial              model
                QzNDME1SM0QzNQ==    10.201.209.15           SWCORE_CECOM2  C3C0MR3D35  SAL1703WZ27         WS-C6506-E
                             NaN    10.201.209.18            000c291e3a3c         NaN          NaN      Cisco-VM-SPID
                             NaN     10.201.70.21              cecomsdnaa         NaN          NaN             VMware
        -------------------------------------------------------------------------------------------------------------
            - df_links =
                     tgtDevice   tgtIfName srcIfName      srcDevice
                  000c291e3a3c        eth0     Gi2/4  SWCORE_CECOM2
                    cecomsdnaa        eth0    Gi2/20  SWCORE_CECOM2
        Nexus-S2X(FOC22431T1E)     Eth1/27    Gi2/29  SWCORE_CECOM2
        """
        text = json.dumps(cdp_table_textfsm)
        text = text.replace('TenGigabitEthernet', 'Te')
        text = text.replace('GigabitEthernet', 'Gi')
        text = text.replace('FastEthernet', 'Fa')
        text = text.replace('Ethernet', 'Eth')
        df = pd.DataFrame(json.loads(text))
        for index in range(df.shape[0]):
            #del s2wcore.sedena.gob.mx
            df.iloc[index, 0] = df.iloc[index, 0].split('.')[0]
            #del Cisco CISCO3945-CHASSIS (platform column)
            name_split = df.iloc[index, 2].split(' ')
            name2nd = name_split[1:] if len(name_split)>1 else name_split
            df.iloc[index, 2] = "".join(name2nd)
        #breakpoint()    
        df=df.iloc[:,[0,1,2,3,4]]
        # Nodes
        df.rename(columns={'destination_host': 'name', 'management_ip': 'hostname', 'platform':'model'}, inplace=True)
        df['tipo']='cdp'
        self.df_nodes = self.df_nodes.append( df.drop_duplicates(subset ="name", keep = 'first', inplace = False).iloc[:,[0,1,2,5]])

        # Links
        df.rename(columns={'name': 'tgtDevice', 'remote_port': 'tgtIfName', 'local_port':'srcIfName'}, inplace=True)
        df=df.iloc[:,[0,3,4]]
        df['srcDevice']=self.cli_name
        df['source'] = df['srcIfName'] + '@' + df['srcDevice']
        df['target'] = df['tgtIfName'] + '@' + df['tgtDevice']
        df['links'] = ''

        for index in range(df.shape[0]):
            if index==0:
                df.iloc[index, 6] = [frozenset({df.iloc[index, 5], df.iloc[index, 4]  })]
                #df.iloc[index, 6] = [{df.iloc[index, 5], df.iloc[index, 4]  }]
            else:
                df.iloc[index, 6] = frozenset({df.iloc[index, 5], df.iloc[index, 4]  })
            self.df_links = df.iloc[:,[0,1,2,3,6]]



class topologyData:
    def __init__(self):
        self.df_nodes = pd.DataFrame()
        self.df_links = pd.DataFrame()
        self.df_nodeSet = pd.DataFrame()
        self.df_nodesJS = pd.DataFrame()
        self.df_linksJS = pd.DataFrame()
        self.df_nodeSetJS = pd.DataFrame()
        self.topology = {
            "nodes":[],
            "links":[],
            "nodeSet":[]
        }
    #Nodes
    def add_nodes(self, df_nodes):
        """
        - Add node from each Devices Class to NextUI
        - Verify no duplicates
        """
        self.df_nodes=self.df_nodes.append(df_nodes)
        self.df_nodes.sort_values(["username"], ascending = (False), inplace=True)
        self.df_nodes.drop_duplicates(subset=["name"], keep='first', inplace=True)

    def add_js(self, path='NextUI/topology.js'):
        """
        - Lee la información de NextUI/static/js/topology.js
        - Guarda la informacion en las variables: self.df_nodesJS, self.df_nodeSetJS, self.df_linksJS
        """
        try:
            with open (path, 'r') as f:
                text=f.read()
                text=text.split('topologyData = ')[1]
                topologyData = json.loads(text)
            self.df_nodesJS = pd.DataFrame(topologyData['nodes'])
            self.df_nodeSetJS = pd.DataFrame(topologyData['nodeSet'])
            self.df_linksJS = pd.DataFrame(topologyData['links'])
        except:
            pass

    #Links
    def add_links(self, df_links):
        """
        - Add link from each Devics Class to NextUI.topologyData
        - Verify no duplicates
        """
        self.df_links=self.df_links.append(df_links)
        self.df_links.sort_values(["srcDevice", "tgtDevice"], ascending = (True, True), inplace=True)
        self.df_links.drop_duplicates(subset="links", keep='first', inplace=True)


    #NextUI
    def combinar_topologyJS(self):
        """
        - Combinar posicion y nodos manuales
        """

        df=pd.merge(self.df_nodes, self.df_nodesJS, on=['name'], how='left',  suffixes=('', '_'))
        try:
            # quitar columnas con '_'. Error cuando ejecutado por primera vez y no existen columnas x, y
            self.df_nodes=df.loc[:, ['name', 'hostname', 'username', 'password', 'encoded_password', 'tipo', 'connection', 'serial','model', 'icon', 'vlan', 'x', 'y']]
            df_manualJS = self.df_nodesJS[self.df_nodesJS['tipo']=='manual']
            df_manualJS = df_manualJS.loc[:, ['name', 'hostname', 'username', 'password', 'encoded_password', 'tipo',
                                                                 'connection', 'serial', 'model', 'icon', 'vlan', 'x', 'y']]
            self.df_nodes= self.df_nodes.append(df_manualJS)
        except:
            pass


    def depurar_links(self):
        """
        - Agrega al  dataframe de los links, las columnas: source y target
        - Agrega a los dataframes (link y nodes), una columna con su id.
        """
        self.df_nodes.reset_index(inplace=True)
        self.df_nodes['id']= self.df_nodes.index
        try:
            # x,y causan conflicto si no estan grabadas las posiciones
            self.df_nodes=self.df_nodes.loc[:,['id', 'name', 'hostname', 'username', 'password', 'encoded_password', 'tipo', 'connection', 'serial', 'model', 'icon', 'vlan', 'x','y' ]]
        except:
            pass
        self.df_links=pd.merge(self.df_nodes.loc[:,['name', 'id']], self.df_links, how='right', left_on='name', right_on='tgtDevice')
        self.df_links.rename(columns={'id': 'target'}, inplace=True)
        self.df_links=pd.merge(self.df_nodes.loc[:,['name', 'id']], self.df_links, how='right', left_on='name', right_on='srcDevice')
        self.df_links.rename(columns={'id': 'source'}, inplace=True)
        self.df_links.reset_index(inplace=True)
        self.df_links['id']=self.df_links.index
        self.df_links=self.df_links.loc[:,['id','source', 'srcDevice','srcIfName','target','tgtDevice','tgtIfName']]

    def to_file(self, path='NextUI/topology.js'):
        """
        - Guardar la informacion en topology.js
        - Pasa la infomracion a un diccionario
        - Guardar topology.js anterior como .bkp con un timestamp
        """
        dt_now=datetime.datetime.now()
        fecha=dt_now.strftime('%d-%b-%Y-%H-%M')
        topologyData={'nodes':self.df_nodes.to_dict('records'), 'links':self.df_links.to_dict('records'), 'nodeSet':self.df_nodeSet.to_dict('records')}
        with open (path, 'w') as f:
            texto=json.dumps(topologyData, indent = 2)
            f.write('var topologyData = ' + texto)