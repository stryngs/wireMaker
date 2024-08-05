# What is this?
A wrapper for creating on-the-fly WireGuard configurations

# What does it do?
This code created the files necessary for a quick wireguard setup.

# Single client setup.
The default IP range built into this is for a 10.249.177.1 as the server and a 10.249.177.2 as the client.

# Multiple client setup.
Uses the same layout on the server side as the single client setup with the addition of being able to generate configurations for multiple clients.  This is achieved by using `-m` and providing a number from 3 to 254.  As an example if you did `-m 10` then you would create 9 different client files.  The ip address granted to cliWire-4.conf would be a `10.249.177.4`.

# How?
```
## Server setup:
    wg-quick up ./svrWire.conf
    ifconfig svrWire 10.249.177.1 up

## Client setup:
    wg-quick up ./cliWire.conf

## Server teardown:
    wg-quick down ./svrWire.conf

## Client teardown:
    wg-quick down ./cliWire.conf
```
