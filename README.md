# editing_proxy_config
how to edit proxy config using python

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
  
The expected output: 

![image](https://user-images.githubusercontent.com/94804863/160229376-93e9069c-4d06-4438-a3d7-653ada884144.png)

