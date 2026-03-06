# libraries 
import socket 
import os 
import platform 
import threading 
import time 
import concurrent.futures 






# function to scan ports 
def scan_port( target , port ):
    s = socket.socket ( socket.AF_INET ,socket.SOCK_STREAM)
    s.settimeout( 1 )
    try : 
        result = s.connect_ex ( ( target, port ))
        s.close()
        if result == 0 : 
            return "open"
        else : 
            return "closed"
    except Exception as e : 
        pass 
    finally : 
        s.close()
# fuction to scan ports in range 
def scan_ports ( target , start_port , end_port) : 
    open_ports = []
    for port in range ( start_port , end_port + 1 ) : 
        status = scan_port ( target , port )
        if status == "open": 
            open_ports.append ( port )
    return open_ports

# scan active hosts in the network 
def check_host( ip ):
    s = socket.socket ( socket.AF_INET , socket.SOCK_STREAM)
    s.settimeout(1)
    try : 
        res = s.connect_ex ( ( ip , 80))
        s.close()
        if res == 0 : 
            try : 
                hostname = socket.gethostbyaddr ( ip )[0]
            except socket.herror :
                hostname = "Unknown"
            return ( "up", ip , hostname)
        else : 
            return ( "down", ip, None ) 
    except socket.error :
        return ( "down" , ip , None )
    finally :
        s.close()
def scan_hosts ( mask):
    active_hosts = []
    inactive_hosts = []
    ips = [f"{mask}.{i}" for i in range ( 1, 255)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future = executor.map(check_host , ips)
        for result in future :
            if result[0] == "up" : 
                active_hosts.append ( ( result[1], result[2] ) )
            else : 
                inactive_hosts.append ( result[1] )
    return active_hosts , inactive_hosts



        
        

            
            

            


