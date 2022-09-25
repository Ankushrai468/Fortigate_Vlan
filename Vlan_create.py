import csv
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from pprint import pprint

# in this code we are Creating Vlan on fortigate firewall using Jinja2 templates.

# get the file in fileloader and load into Environment
file_loadr = FileSystemLoader("")
env = Environment(loader=file_loadr)
# create a jinja2 template for vlan and load it into env
template = env.get_template("Fortigate_jinja_template.j2")
# this dict will have site number and vlan ip/mask
FMG_dict_var = {}
# open the csv file which have vlan info and put that into FMG_dict_var(dictonary)
with open ("Vlan_creation.csv","r",encoding='utf-8-sig') as f:
    csv_data = csv.DictReader(f)
    for data in csv_data:
        dict = data
        store_val = input()
        print(store_val)
        for store in dict:
            if dict['Store_code'] == store_val:
                FMG_dict_var = dict
pprint(FMG_dict_var)
# now render the information from csv to jinja2 empty field
output = template.render(port2_72_ip = FMG_dict_var['First_vlan_ip'],
                         port2_72_ip_mask = FMG_dict_var['First_vlan_subnet'],
                        port2_70_ip = FMG_dict_var['Second_Vlan_ip'],
                        port2_70_ip_mask = FMG_dict_var['Second_Vlan_subnet'])
print(output)
# now put the vlan config in text file which have all ip and vdom details in it
with open ("Vlan_Config.txt", "w", encoding="utf-8") as f:
    f.write(output)
# connect to fortigate and push all commands on fortigate through netmiko
Fortigate_Connect = {
    'device_type' : 'fortinet',
    'host' : '10.10.10.10',
    'username' : 'admin',
    'password' : 'admin',
    'port' : 22,
}
ssh = ConnectHandler(**Fortigate_Connect)
send_command = ssh.send_config_from_file("Vlan_Config.txt")
print(send_command)


