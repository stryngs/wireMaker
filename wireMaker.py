#!/usr/bin/python3

import argparse
import os

def peerGen(endIp, endPt, svrPub, cliOct):
    """Generate and return peer information"""
    os.system('umask 077 && wg genkey > cliPrvkey')
    os.system('cat cliPrvkey | wg pubkey > cliPubkey')
    os.system('wg genpsk > psk 2>/dev/null')
    with open('cliPrvkey') as iFile:
        cliPriv = iFile.read().splitlines()[0]
    with open('cliPubkey') as iFile:
        cliPub = iFile.read().splitlines()[0]
    with open('psk') as iFile:
        psk = iFile.read().splitlines()[0]
    cliIp = f'Address = 10.249.177.{cliOct}/24'
    cliQck = f"""[Interface]
PrivateKey = {cliPriv}
{cliIp}

[Peer]
PublicKey = {svrPub}
Endpoint = {endIp}:{endPt}
AllowedIPs = 10.249.177.0/24
PresharedKey = {psk}
"""
    return cliQck, cliPub, psk, cliOct


def main(endIp, endPt, multiClient = False):
    os.system('umask 077 && wg genkey > svrPrvkey')
    os.system('cat svrPrvkey | wg pubkey > svrPubkey')
    with open('svrPrvkey') as iFile:
        svrPriv = iFile.read().splitlines()[0]
    with open('svrPubkey') as iFile:
        svrPub = iFile.read().splitlines()[0]

    ## Create environment for one client
    if multiClient is False:
        cliQck = peerGen(endIp, endPt, svrPub, 2)
        svrQck = f"""[Interface]
PrivateKey = {svrPriv}
ListenPort = {endPt}
Address = 10.249.177.1

[Peer]
PublicKey = {cliQck[1]}
AllowedIPs = 10.249.177.2/32
PresharedKey = {cliQck[2]}
"""

        with open('svrWire.conf', 'w') as oFile:
            oFile.write(f'{svrQck}')
        with open('cliWire.conf', 'w') as oFile:
            oFile.write(f'{cliQck[0]}')

    ## Create environment for multiple clients
    else:
        pList = []
        for i in range (2, multiClient + 1):
            pList.append(peerGen(endIp, endPt, svrPub, i))

        fList = []
        for p in pList:
            cStr = f"""[Peer]
PublicKey = {p[1]}
AllowedIPs = 10.249.177.{p[3]}/32
PresharedKey = {p[2]}
"""
            fList.append(cStr)

        cliStr = '\n'.join(fList)
        svrQck = f"""[Interface]
PrivateKey = {svrPriv}
ListenPort = {endPt}
Address = 10.249.177.1

{cliStr}
"""
        with open('svrWire.conf', 'w') as oFile:
            oFile.write(f'{svrQck}')

        ## Generate client configs
        for i in range(len(pList)):
            with open(f'cliWire-{i + 2}.conf', 'w') as oFile:
                oFile.write(f'{pList[i][0]}')

if __name__ == '__main__':

    ## Inputs
    psr = argparse.ArgumentParser(description = 'A wrapper for creating WireGuard configurations')
    psr.add_argument('-m', help = 'Multi client mode')
    psr.add_argument('-s', help = 'WireGuard server endpoint IP address', required = True)
    psr.add_argument('-p', help = '51820 is the default port')
    args = psr.parse_args()

    ## Parsing
    endIp = args.s
    if args.p is None:
        endPt = 51820
    else:
        endPt = args.p
    if args.m is not None:
        args.m = int(args.m)
        x = main(endIp, endPt, args.m)
    else:
        main(endIp, endPt)

    ## Cleanup    
    os.remove('cliPrvkey')
    os.remove('cliPubkey')
    os.remove('svrPrvkey')
    os.remove('svrPubkey')
    os.remove('psk')
