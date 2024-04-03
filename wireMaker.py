#!/usr/bin/python3

import argparse
import os

def main(endIp, endPt):

    ## Key fun
    os.system('umask 077 && wg genkey > svrPrvkey')
    os.system('cat svrPrvkey | wg pubkey > svrPubkey')
    os.system('umask 077 && wg genkey > cliPrvkey')
    os.system('cat cliPrvkey | wg pubkey > cliPubkey')
    # os.system('wg genpsk > psk 2>/dev/null')

    ## Shh
    with open('svrPrvkey') as iFile:
        svrPriv = iFile.read().splitlines()[0]
    with open('svrPubkey') as iFile:
        svrPub = iFile.read().splitlines()[0]
    with open('cliPrvkey') as iFile:
        cliPriv = iFile.read().splitlines()[0]
    with open('cliPubkey') as iFile:
        cliPub = iFile.read().splitlines()[0]
    # with open('psk') as iFile:
    #     psk = iFile.read().splitlines()[0]

    ## quick setups
    svrQck = f"""[Interface]
PrivateKey = {svrPriv}
ListenPort = {endPt}

[Peer]
PublicKey = {cliPub}
AllowedIPs = 10.249.177.2/32
"""
    cliQck = f"""[Interface]
PrivateKey = {cliPriv}
Address = 10.249.177.2/24
DNS = 9.9.9.9, 1.1.1.1

[Peer]
PublicKey = {svrPub}
Endpoint = {endIp}:{endPt}
AllowedIPs = 10.249.177.0/24
"""
    with open('svrWire.conf', 'w') as oFile:
        oFile.write(f'{svrQck}')
    with open('cliWire.conf', 'w') as oFile:
        oFile.write(f'{cliQck}')

if __name__ == '__main__':

    ## Inputs
    psr = argparse.ArgumentParser(description = 'A wrapper for creating WireGuard configurations')
    psr.add_argument('-s', help = 'WireGuard server endpoint IP address', required = True)
    psr.add_argument('-p', help = '51820 is the default port')
    args = psr.parse_args()

    ## Parsing
    endIp = args.s
    if args.p is None:
        endPt = 51820
    else:
        endPt = args.p

    ## Run
    main(endIp, endPt)
    os.remove('cliPrvkey')
    os.remove('cliPubkey')
    os.remove('svrPrvkey')
    os.remove('svrPubkey')
