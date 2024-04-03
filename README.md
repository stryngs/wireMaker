# What is this?
A wrapper for creating on-the-fly WireGuard configurations

# What does it do?
This code created the files necessary for a quick setup server and client side for wireguard.

The default IP range built into this is for a 10.249.177.1 as the server and a 10.249.177.2 as the client.  Lines 38 and 44 will be of interest in this regard.

# How?
```
## Server setup:
    ip link add dev svrWire type wireguard
    ip address add dev svrWire 10.249.177.1/24
    wg setconf svrWire ./svrWire.conf
    ifconfig svrWire up

## Client setup:
    wg-quick up ./cliWire.conf

## Server teardown:
    ip link delete svrWire

## Client teardown:
    ip link delete cliWire
```
