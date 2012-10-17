#Proxmoxia <small>A pythonic wrapper for Proxmox REST API</small>

##What does it do and what's different?

Proxmoxia is a wrapper around the [Proxmox REST API](http://pve.proxmox.com/pve2-api-doc/). It is intended to be used by administrators and users who need to access information about their proxmox cluster which they might otherwise have read/scraped from the web UI.

As well as providing direct access to the REST api via fetch, post and put methods objects are provided which are built ontop of the api. For example the nodes.OpenVZ class provides start/stop methods which will query and return the status and log of the triggered task which the the start request will have initiated.

##Connecting to Proxmox

The first thing to do is import the proxmox library and create a Connection to the server. This connection will be used to authenticate ourselves and can be any of the nodes in the cluster.

````python
import proxmox

PROXMOX_HOST = "proxmox-1"  # can also be an IP or the FQDN of the host
PROXMOX_PORT = 8006	

connection = proxmox.Connector(PROXMOX_HOST, PROXMOX_PORT)
````

Once you have connected you should use the connection to retrieve an AuthenticationToken. This is stored on your connection object for later use, but also returned for you to inspect.

````python
auth_token = connection.fetch_auth_token('user@pam', 'strawberries')
````

##Simple query based access

````python
for node in connection.fetch('nodes'):
    for vm in connection.fetch('nodes/%s/openvz' % node['node']):
        print "%s. %s => %s" % (vm['vmid'], vm['name'], vm['status'])

>>> 141. puppet-2.london.baseblack.com => running
   101. munki.london.baseblack.com => running
   102. redmine.london.baseblack.com => running
   140. dns-1.london.baseblack.com => running
   126. ns-3.london.baseblack.com => running
   113. rabbitmq.london.baseblack.com => running
````

##Class based access

Classes exist for a number of entities within Proxmox. For example, there is a Node class which represents a single node within the cluster. Or an OpenVZ class which represents a single openvz container in the cluster.

###Dynamic GET methods

Any endpoints which are accessed via a GET request are dynamically generated upon call. 
For example the `proxmox.Node().rrd(ds='cpu', timeframe='hour')` creates an AttrMethod object when the rrd method cannot be found within the Node Classes scope.

These methods are recursive so `proxmox.Node(conn, 'proxmox-7).scan.nfs(server="homes-nfs")` will generate a valid call.

##Examples:

* Connect to a specific node and access end points on it.

````python
    node = proxmox.Node(connection, 'proxmox-7')
    print node.rrd(ds='cpu',timeframe='hour')
    >>>{u'filename': u'/var/lib/rrdcached/db/pve2-node/proxmox-7.png'}
````
    
* Create an OpenVZ object for VM with vmid=108 and generate the 'status/current' request.

````python
    print node.openvz(108).status.current()
    >>>{u'status': u'stopped', u'uptime': 0, u'disk': 0, u'maxswap': 536870912, u'name': u'packages.london.baseblack.com', u'diskread': 0, u'diskwrite': 0, u'ip': u'192.168.123.108', u'netin': 0, u'cpus': 1, u'mem': 0, u'failcnt': 0, u'swap': 0, u'nproc': 0, u'netout': 0, u'ha': 0, u'type': u'openvz', u'cpu': 0, u'maxdisk': 4294967296, u'maxmem': 536870912}

* Create and execution task. Control is returned after the task has completed. *Note: This is presently a blocking call*

````python
    status, log = node.openvz(108).start()
    
    print status
    >>>{u'status': u'stopped', u'node': u'proxmox-7', u'pstart': 115470859, u'upid': u'UPID:proxmox-7:00009766:06E1F20B:507853E7:vzstart:108:root@pam:', u'pid': 38758, u'user': u'root@pam', u'starttime': 1350063079, u'type': u'vzstart', u'id': u'108'}
    
    print log
    >>>[u'Starting container ...', u'Container is mounted', u'Adding IP address(es): 192.168.123.108', u'Setting CPU units: 1000', u'Setting CPUs: 1', u'Container start in progress...', u'TASK OK']
````

		
