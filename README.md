# port-forward

Set of Python scripts which automates the port-forwarding configuration on hosts running a set of virtual machines. 

This set of simple Python scripts helps on configuring port-forwarding through a host, allowing accessing a virtual machine with a private IP.

For example, suppose you have only one public IP like 123.456.7.8 and all your VMs has address ranging from 198.162.122.10 to 192.168.122.20.

So, how do you access those VMs with an internal IP? Port-forwading helps to solve this issue:

##Set

iptables -t nat -A PREROUTING -p tcp --dport %<PORT> -j DNAT --to %<IP>:22
iptables -I FORWARD -d %<IP>/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT

*where:
22 is the VM port you want as target.
PORT is the host port which will be mapped to the port 22.
IP is the VM internal IP.*

##Unset

iptables -t nat -D PREROUTING -p tcp --dport %<PORT> -j DNAT --to %<IP>:22
iptables -D FORWARD -d %IP/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT

*where
22 is the VM port you want as target.
PORT is the host port which will be mapped to the port 22.
IP is the VM internal IP.*