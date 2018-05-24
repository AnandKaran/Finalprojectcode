""" I have written this code myself , taken help from gns3api documentation for the structure"""
import requests
import json

nat = '{"symbol": ":/symbols/cloud.svg","name": "NAT","node_type":"nat", "compute_id":"local"}'
switch = '{"symbol": ":/symbols/ethernet_switch.svg","name": "Switch", "node_type": "ethernet_switch", "compute_id": "local"}'
router1 = "{\"symbol\": \":/symbols/router.svg\",\"name\": \"R1\", \"properties\": {\"platform\": \"c3745\", \"nvram\": 256, \"image\": \"c3745-advipservicesk9-mz.124-19.bin\", \"ram\": 256, \"system_id\": \"FTX0945W0MY\", \"slot0\": \"GT96100-FE\",\"slot1\": \"NM-1FE-TX\",\"slot2\": \"NM-4T\", \"idlepc\": \"0x62b20e20\"}, \"compute_id\": \"local\", \"node_type\": \"dynamips\"}"
L2switch = '{"symbol":":/symbols/multilayer_switch.svg","node_type": "qemu", "compute_id": "local", "name": "Cisco IOSvL2 15.2.4055", "properties": {"hda_disk_image": "IOSv-L2.qcow2", "ram": 768, "qemu_path": "qemu-system-x86_64","adapters":16}}'


def create_node(d):#creates a node
    url = "http://localhost:3080/v2/projects/" + proj_id + "/nodes"
    print(url)
    headers = {
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=d, headers=headers)

    print("Test project" + response.text)



name= input("Enter the project name:" )
p = {"name": name}
def create_projects(p):#creates a project in GNS3 directory
    url = "http://localhost:3080/v2/projects"
    global name
    resp = requests.post(url,json.dumps(p))
    print("\nRaw response from Get request:\n", resp.text)

def get_project_id():#gets project id
    url = "http://localhost:3080/v2/projects"
    resp = requests.get(url, verify=False).json()

    for i in resp:
        if i['name'] == name:
            global proj_id
            proj_id = i['project_id']
            print(proj_id)
            return proj_id

def get_nodeid():#gets node id which are created,stored as a list
    global l
    l=[]
    url = "http://localhost:3080/v2/projects/" + proj_id + "/nodes"
    resp = requests.get(url, verify=False).json()
    print(resp)
    global nodeid
    for i in resp:
        if i['name'] == i['label']['text']:
            nodeid = i["node_id"]
            l.append(nodeid)
    print(l)

def link_nodes():#link nodes by accessing the elements of list of node ids
    global l
    url = 'http://localhost:3080/v2/projects/' + proj_id + '/links'
    print(url)
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Postman-Token': '70502477-7a57-466a-a895-40c25e1109b9',
    }

    data = {"nodes": [{"adapter_number": 0, "node_id": l[0], "port_number": 0},
                      {"adapter_number": 0, "node_id": l[1], "port_number": 0}]}
    data2 = {"nodes": [{"adapter_number": 0, "node_id": l[1], "port_number": 1},
                       {"adapter_number": 0, "node_id": l[2], "port_number": 0}]}
    data3 = {"nodes": [{"adapter_number": 1, "node_id": l[2], "port_number": 0},
                       {"adapter_number": 0, "node_id": l[3], "port_number": 0}]}
    print (data)
    print (data2)
    print (data3)
    response1 = requests.post(url, json.dumps(data), headers=headers)
    res_out = response1.json()
    response2 = requests.post(url, json.dumps(data2), headers=headers)
    res_in = response2.json()
    response3 = requests.post(url, json.dumps(data3), headers=headers)
    res_i = response3.json()
    print(res_i)
    # print(res_out.text)


def createl2qemuswitch(d):#creates a l2 qemu switch
    url = 'http://localhost:3080/v2/projects/' + proj_id + '/nodes'
    print(url)
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Postman-Token': '3f1683c0-986f-464d-afef-f96ed4e2eca3',
    }

    print(d)

    response = requests.post(url=url, headers=headers, data=d)
    print(response.json())


def startnodes():#to start nodes
    for i in range(0,len(l)):
        url="http://localhost:3080/v2/projects/"+proj_id+"/nodes/"+ l[i] +"/start"
        headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Postman-Token': '9ccf38c8-df8c-40a9-803a-41820eaf843d',
        }
        response = requests.post(url=url,headers=headers)


create_projects(p)
get_project_id()
create_node(nat)
create_node(switch)
n=int(input("Enter the number of L2 switches you want:"))
def l2switches():
    for i in range (n):
        createl2qemuswitch(L2switch)
l2switches()

n=int(input("Enter the number of routers you want:"))
def router():
    for i in range(n):
        create_node(router1)

router()
get_nodeid()
link_nodes()
startnodes()

