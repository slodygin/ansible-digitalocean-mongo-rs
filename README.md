# 
# Sample Ansible Playbook to setup mongodb cluster on DigitalOcean  and test failover
Cluster will be created with 3 nodes (master,slave and arbitr).
This is extended script. Source is here 
(https://github.com/jasonheecs/ansible-digitalocean-sample-playbooks.git).

## Prerequisites

Ansible >= 2.4.0.0

## Usage
0) Ssh public key  from your DigitalOcean (Security >SSH Key) will be added to new droplets. 
You should use this key for authentification.
 
1) Clone this repo:
```
git clone https://github.com/slodygin/ansible-digitalocean-mongo-rs.git
cd ansible-digitalocean-mongo-rs
```

2) Rename the `group_vars/all/secret.yml.example` file to `group_vars/all/secret.yml` and change the secret variables to your appropriate values.

3) Modify the values in `group_vars/all/main.yml` with your desired values.
(do_api_token - token, user_acct_password - password for ssh user )

4) Run the following:
```
ansible-galaxy install -r requirements.yml
ansible-playbook -i hosts main.yml
```
5) You can check cluster on mongo-test1
```
mongo --port 27017 --username siteRootAdmin --password passw0rd admin
rs.conf()
rs.printReplicationInfo()
rs.printSlaveReplicationInfo()
```

## Failover testing 

1) ensure you can ping mongo-test1,mongo-test2 and mongo-test3
```
ping mongo-test1
ping mongo-test2
ping mongo-test3 
```
2) execute script
```
apt-get install python-pymongo
./test/test_repl.py
```
3) on mongo-test1  stop primary:
```
iptables -I INPUT -p tcp --dport 27017 -j REJECT
or
service mongod stop
```
4)you should see all exceptions during failover

5) on mongo-test1 restore access
``` 
iptables -D INPUT -p tcp --dport 27017 -j REJECT
or
service mongod start
```
6) on mongo-test2 swkitch to old primary
```
mongo --port 27017 --username siteRootAdmin --password passw0rd admin
cfg = rs.conf()
cfg.members[0].priority = 1
cfg.members[1].priority = 0.5
cfg.members[2].priority = 0.5
rs.reconfig(cfg)
```





