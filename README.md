#Proxmoxia <small>A pythonic wrapper for Proxmox REST API</small>

##What does it do and what's different?

Proxmoxia is a wrapper around the [Proxmox REST API](http://pve.proxmox.com/pve2-api-doc/). It is intended to be used by administrators and users who need to access information about their proxmox cluster which they might otherwise have read/scraped from the web UI.

Rather than writing wrappers for each individual end point and method combination in the API we've instead created a dynamic method call which responds to the attribute you've attempted to reach.

We'll outline how this works later in the doc.

#First Steps: 
##Connecting to Proxmox

The first thing to do is import the proxmox library and create a Connection to the server. This connection will be used to authenticate ourselves and can be any of the nodes in the cluster.

````python
import proxmox

PROXMOX_HOST = "proxmox-1"  # can also be an IP or the FQDN of the host
PROXMOX_PORT = 8006	

connection = proxmox.Connector(PROXMOX_HOST, PROXMOX_PORT)
````

Once you have connected you should use the connection to retrieve an AuthenticationToken. 

````python
auth_token = connection.get_auth_token('user@pam', 'strawberries')
````

This is stored on your connection object for later use, but also returned for you to inspect. 

**Note** Due to the __repr__ method which is on the AuthToken object returned, unless you assign it to a variable it will be printed out into your stdout.

##Simple query based access

Queries are exposed via the access methods **get**, **post**, **put** and **delete**.
The filter path is relative to the api root passed to the connection constructor.

````python
for node in connection.get('nodes'):
    for vm in connection.get('nodes/%s/openvz' % node['node']):
        print "%s. %s => %s" % (vm['vmid'], vm['name'], vm['status'])

>>> 141. puppet-2.london.baseblack.com => running
    101. munki.london.baseblack.com => running
    102. redmine.london.baseblack.com => running
    140. dns-1.london.baseblack.com => running
    126. ns-3.london.baseblack.com => running
    113. rabbitmq.london.baseblack.com => running
````

##Attribute based access

Having to continually build up your url in bits is a little ass. So we also have an attribute call based mechanism for reaching endpoints.

When an attribute is accessed on a proxmox.Proxmox or proxmox.Node object it will generate a new AttrMethod based object. These methods are recursive so `p.cluster.config()` will generate a valid GET request.

_**Note** proxmox.Node is a convience class provided to wrap up `proxmox.Proxmox(c).nodes(nodename)`. It may also be used to extend the class with an execution method. TBD._

###Get/Post/Put and Delete requests

The default request made when an attribute is called is a GET request. So p.nodes() will create a GET attrMethod and call it with no arguments. The url it will generate will be:

    http://SERVER:PORT/api2/json/nodes?

Another way of specifying a Get request should be made is to call .get() on the attribute you want. ie. `p.nodes.get()`.

To request a Post/Put or Delete, append the call instead with the matching name:

````python
p.nodes.post()
p.nodes.put()
p.nodes.delete()
````

###Named attributes
Some attributes such as a node name or virtual machine id which you do not know before you start writing your code are harder to address as a simple attribute. You could use an inline eval, but they stick out like a sore thumb in this context.

So to handle these, each AttrMethod accepts a non-keyword argument which it will use to generate a the new AttrMethod for. For example these lines are functionally identical:

````python
result = node.openvz.108.status.current()

vmid = 108
result = eval('node.openvz.%d.status.current()' % vmid)
result = node.openvz(vmid).status.current()
````

###Request Parameters + Arguments
Some of the API endpoints require a number of keyword arguments. For these address each as a named parameter  in your attribute call. In this example `node.rrd(ds='cpu', timeframe='hour')` will generate a Get request encoding the arguments into a url like this:

    http://SERVER:PORT/api2/json/nodes/proxmox-7/rrd?ds=cpu&timeframe=hour

`node.rrd.post(ds='cpu', timeframe='hour')` would generate a Post request with a url/post fields like this:

    url = http://SERVER:PORT/api2/json/nodes/proxmox-7/rrd?
    post_fields = ds=cpu&timeframe=hour

Put/Delete requests are the same as posts.

##Examples:

* Create Proxmox and Node access objects:

````python
p = p = proxmox.Proxmox(connection)
node = proxmox.Node(connection, 'proxmox-7')
````

* Connect to a access end points on a node:

````python
print node.rrd(ds='cpu',timeframe='hour')
>>>{u'filename': u'/var/lib/rrdcached/db/pve2-node/proxmox-7.png'}
````
    
* Requests the status on a vm with id number 108:

````python
vmid = 108
print node.openvz(vmid).status.current()
>>>{u'status': u'stopped', u'uptime': 0, u'disk': 0, u'maxswap': 536870912, u'name': u'packages.london.baseblack.com', u'diskread': 0, u'diskwrite': 0, u'ip': u'192.168.123.108', u'netin': 0, u'cpus': 1, u'mem': 0, u'failcnt': 0, u'swap': 0, u'nproc': 0, u'netout': 0, u'ha': 0, u'type': u'openvz', u'cpu': 0, u'maxdisk': 4294967296, u'maxmem': 536870912}
````

* Find a vm template filepath and use this as the ostemplate for a new vm you create. 
  And then start it up once it has finished being created:

````python
# find the path for the template you want to use.
for template in node.storage('virtual-nfs').content(content='vztmpl'):
    if re.match('.*ubuntu-12.04-bb-20121010b_amd64.tar.gz$', template['volid']):
        volume = node.storage('virtual-nfs').content(template['volid']).get()

# create the container, giving it some sensible settings
taskid = node.openvz.post( ostemplate=volume.get('path'),
                           vmid=204,
                           hostname='test-4',
                           ip_address='192.168.123.204',
                           storage='local')

# keep an eye on task and see when its completed
while node.tasks(taskid).status()['status'] == 'running':
        time.sleep(1)

# print out the logs
for line in node.tasks(taskid).log():
    print line['t']

try:
    # start up the container
    node.openvz('204').status.start.post()
except:
    raise Exception('Unable to start container')
````

* Find if a user exists and create them if they do not:

````python
if 'andrew.bunday@pve' not in [x['userid'] for x in p.access.users()]:
    p.access.users.post(userid='andrew.bunday@pve', comment="test user", password="strawberries")
````