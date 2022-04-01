from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, DefaultController
from mininet.link import TCLink
from mininet.util import  dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import os
import subprocess
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

global driver

class DumbellTopo(Topo):
    "Two switches connected to two clients and a server in a dumbell topology"
    def build(self):
        cli_switch = self.addSwitch('s1', stp=True)
        serv_switch = self.addSwitch('s2', stp=True)
        cli1 = self.addHost('cli1')
        cli2 = self.addHost('cli2')
        serv = self.addHost('serv')
        self.addLink(cli1, cli_switch, bw=5)
        self.addLink(cli2, cli_switch, bw=5)
        self.addLink(serv, serv_switch, bw=5)
        self.addLink(cli_switch, serv_switch, bw=5)
        # self.addLink(cli1, cli2)
        # self.addLink(cli1, serv)

        # for h in range(n):
        #         host = self.addHost('h%s' %(h+1), cpu=.5/n)
        #         self.addLink(host, switch, bw=10, loss=2)

def changeBandwidth(node, new_bw):
    for intf in node.intfList(): # loop on interfaces of node
    #info( ' %s:'%intf )
        if intf.link: # get link that connects to interface(if any)
            intfs = [ intf.link.intf1, intf.link.intf2 ] #intfs[0] is source of link and intfs[1] is dst of link
            intfs[0].config(bw=new_bw) 
            intfs[1].config(bw=new_bw)


"Create network and run simple performance test"
def start():
    topo = DumbellTopo()
    net = Mininet(topo, host=CPULimitedHost, link=TCLink, controller=DefaultController)
    perfTest(net)


def perfTest(net):
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing bandwidth between h1 and h4")
    cli1, cli2, serv = net.get('cli1', 'cli2', 'serv')
    serv.setIP('web-platform.test/24')
    hosts = []
    hosts.extend([cli1,cli2,serv])
    for i in range(3):
        result = hosts[i].cmd("ifconfig -a | grep 'ether' | awk ' {print $2}'")
        print("MAC address of host " + str(hosts[i]) + ": " + result)
    cli1, cli2, serv = net.get('cli1', 'cli2', 'serv')
    cli1.popen('google-chrome --no-sandbox')
    CLI(net)
    

if __name__ == '__main__':
    setLogLevel('info')
    start()


