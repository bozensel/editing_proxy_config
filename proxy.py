from ttp import ttp
import json

data_to_parse = """
global
    log                 127.0.0.1 local0
    chroot              /var/lib/haproxy
    pidfile             /var/run/haproxy.pid
    maxconn         4000
    user                haproxy
    group               haproxy
    daemon
defaults
    mode                        http
    log                         global
    option                      httplog
    option                      dontlognull
    option             http-server-close
    option     forwardfor       except 127.0.0.0/8
    option                      redispatch
    retries                     3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client              1m
    timeout server          1m
    timeout http-keep-alive     10s
    timeout check           10s
listen apache-30101
  bind 10.16.79.55:30101
  mode tcp
  balance source
  server cfme1 10.10.10.60:20101 check inter 2s
  server cfme2 10.10.10.61:20101  check backup inter 2s
"""

def haproxy_cfg_parser(data_to_parse): # It parses the following additional unneeded line "  Svc: 307006600 65035   483570    0 0148d14h  2/2/8 (IPv4)". 
    ttp_template = template_haproxy_cfg

    parser = ttp(data=data_to_parse, template=ttp_template)
    parser.parse()

    # print result in JSON format
    results = parser.result(format='json')[0]
    #print(results)

    #converting str to json. 
    result = json.loads(results)

    return(result)

parsed_haproxy_cfg_parser = haproxy_cfg_parser(data_to_parse)

#print(parsed_haproxy_cfg_parser[0]['HAPROXY_CFG'])

for i in parsed_haproxy_cfg_parser[0]['HAPROXY_CFG']:
    #print(i)
    if 'backup' in i: # It gives information from backup server
        #print(i)
        print("The new primary:")
        print(f"server {i['CFM']} {i['IP']} {i['check']} {i['inter']} {i['1s']}") # backup converted to primary.
    elif 'backup' not in i: # It gives information from primary server
        #print(i)
        print("The new secondary:")
        print(f"server {i['CFM']} {i['IP']} {i['check']} backup {i['inter']} {i['1s']}") # primary converted to backup.

############## The expected output ############
'''   
The following config needs to be changed as STEP 2. 

data_to_parse = """
global
    log                 127.0.0.1 local0
    chroot              /var/lib/haproxy
    pidfile             /var/run/haproxy.pid
    maxconn         5000
    user                haproxy
    group               haproxy
    daemon
defaults
    mode                        http
    log                         global
    option                      httplog
    option                      dontlognull
    option             http-server-close
    option     forwardfor       except 127.0.0.0/8
    option                      redispatch
    retries                     3
    timeout http-request    11s
    timeout queue           1m
    timeout connect         12s
    timeout client              1m
    timeout server          1m
    timeout http-keep-alive     10s
    timeout check           10s
listen apache-20101
  bind 10.10.71.56:20101
  mode tcp
  balance source
  server cfme1 10.10.10.60:20101 check inter 2s <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  server cfme2 10.10.10.61:20101  check backup inter 2s <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  
  STEP 2)
  
  It needs to be converted to following: (Primary to secondary --> Secondary to primary)
  
  server cfme1 10.10.10.60:20101 check backup inter 2s
  server cfme2 10.10.10.61:20101 check inter 2s
  
'''
