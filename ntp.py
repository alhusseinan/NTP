#Script to automate NTP configuration on IOS XE devices.
import requests
import json
from datetime import datetime
import csv
import urllib3
urllib3.disable_warnings()

def ntp(username, password,ip_addr, restconf_port, headers, confgen_params, confgen_response):

    restconf_base_url = f"https://{ip_addr}:{restconf_port}/restconf/data"
    ntp_dir = "Cisco-IOS-XE-native:native/ntp"

    # Static values. They should be received via API call to CONFGEN application.

    #Chequeo si existe la VRF de management (siempre tiene el mismo nombre) - "VRF02", y dependiendo de eso voy por un camino o el otro.
    vrf_dir = "/Cisco-IOS-XE-native:native/ip/vrf"
    vrf_list = []
    try:
        vrf_list_dict = requests.get(url=f"{restconf_base_url}/{vrf_dir}", headers= headers, auth=(username, password), verify= False).json()["Cisco-IOS-XE-native:vrf"]
        for vrf in vrf_list_dict:
            vrf_list.append(vrf["name"])
    except:
        print("-> No VRFs configured!")

    vrf_name = "VRF-1"

    if vrf_name in vrf_list:
        #Agregar server-list - Existe VRF
        ntp_config = {
        "Cisco-IOS-XE-native:ntp": {
            "Cisco-IOS-XE-ntp:authenticate": [
                None
            ],
            "Cisco-IOS-XE-ntp:authentication-key": [
                {
                    "number": 24,
                    "md5": confgen_response["ntp_parameters"]["ntp_key_hashed"],
                    "encryption-type": 7
                }
            ],
            "Cisco-IOS-XE-ntp:server": {
                "vrf": [
                    {
                        "name": vrf_name,
                        "server-list": [
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_1"],
                                "key": 24
                            },
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_2"],
                                "key": 24
                            },
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_3"],
                                "key": 24
                            },
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_4"],
                                "key": 24
                            }
                        ]
                    }
                ]
            },
            "Cisco-IOS-XE-ntp:source": {
                confgen_params["mgmt_interface"].split(" ")[0]: confgen_params["mgmt_interface"].split(" ")[1]
            },
            "Cisco-IOS-XE-ntp:trusted-key": [
                {
                    "number": 24
                }
            ]
        }
        }
    else:
        #Agregar server-list - No existe VRF
        ntp_config = {
        "Cisco-IOS-XE-native:ntp": {
            "Cisco-IOS-XE-ntp:authenticate": [
                None
            ],
            "Cisco-IOS-XE-ntp:authentication-key": [
                {
                    "number": 24,
                    "md5": confgen_response["ntp_parameters"]["ntp_key_hashed"],
                    "encryption-type": 7
                }
            ],
            "Cisco-IOS-XE-ntp:server": {
                "server-list": [
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_1"]
                    },
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_2"]
                    },
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_3"]
                    },
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_4"]
                    }
                ]
            },
            "Cisco-IOS-XE-ntp:source": {
                confgen_params["mgmt_interface"].split(" ")[0]: confgen_params["mgmt_interface"].split(" ")[1]
            },
            "Cisco-IOS-XE-ntp:trusted-key": [
                {
                    "number": 24
                }
            ]
        }
    }

    #Imprimo en terminal c??mo qued?? el ntp_config despu??s de evaluar si exist??a la VRF
    # print(json.dumps(ntp_config, indent=2))

    #Antes enviar la configuraci??n, se escribe un archivo de log con la configuraci??n actual.

    log_file = open ("/Users/amanueli/Documents/DevNet/Scripts/DevNet/SNMP_NTP_SYSLOG/log_ntp.txt", "a")
    log_file.write("\n##################################\n\n")
    log_file.write(f"Current configuration for device {ip_addr}  -   Update: {datetime.now()}\n")

    current_ntp_config = requests.get(url=f"{restconf_base_url}/{ntp_dir}", headers= headers, auth=(username, password), verify= False).content.decode("utf-8") 
    log_file.write(current_ntp_config)
    print(current_ntp_config)
    log_file.close()
    print("-> LOG FILE GENERATED")
    # Se aplica nueva configuraci??n
    send_config = requests.put(url=f"{restconf_base_url}/{ntp_dir}", headers= headers, auth=(username, password), data = json.dumps(ntp_config), verify= False).status_code

    if send_config == 204:
        print("-> SUCCESS! NTP Configured")
    else:
        print("-> Yikes! Something went wrong...")


            #TESTEO
            