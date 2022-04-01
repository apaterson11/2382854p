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
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

global driver

class PeerTopo(Topo):
    "Two switches connected to two clients and a server in a dumbell topology"
    def build(self):
        s1 = self.addSwitch('s1') # peerswitch
        s2 = self.addSwitch('s2') # peerjs switch
        s3 = self.addSwitch('s3') # socket.io switch
        cli1 = self.addHost('cli1')
        cli2 = self.addHost('cli2')
        serv1 = self.addHost('serv1')   # peerjs
        serv2 = self.addHost('serv2')   # socket.io

        self.addLink("cli1", "s1")
        self.addLink("s1", "cli2")

        # self.addLink(cli1, peerjsserv)
        # self.addLink(cli1, socketserv)

        # self.addLink(cli2, peerjsserv)
        # self.addLink(cli2, socketserv)
        self.addLink("s1", "serv1")
        self.addLink("s1", "serv2")

        # self.addLink("cli1", "s3")
        # self.addLink("cli2", "s3")
        # self.addLink("s3", "serv2")

        # cli_switch = self.addSwitch('s1', stp=True)
        # serv_switch = self.addSwitch('s2', stp=True)
        # cli1 = self.addHost('cli1')
        # cli2 = self.addHost('cli2')
        # serv = self.addHost('serv')
        # self.addLink(cli1, cli_switch)
        # self.addLink(cli2, cli_switch)
        
        # self.addLink(serv, serv_switch)
        # self.addLink(cli_switch, serv_switch)
        


        # for h in range(n):
        #         host = self.addHost('h%s' %(h+1), cpu=.5/n)
        #         self.addLink(host, switch, bw=10, loss=2)

def changeCPU(node, new_cpu):
    node.config(cpu=new_cpu)

def stopServer(net):
    serv = net.get('serv')
    serv.stop()
    print("server stopped")
    
"Create network and run simple performance test"
def start():
    cpu_list=[0.2, 0.1]
    # cpu_list=[0.1]
    # cpu_list=[0.1]
    for cpu in cpu_list:
        net = Mininet(PeerTopo(), host=CPULimitedHost, link=TCLink, controller=DefaultController)
        nodes = net.hosts
        net.start()
        cli1, cli2 = net.get('cli1', 'cli2',)
        changeCPU(cli1, cpu)
        changeCPU(cli2, cpu)

        f = open("results.csv", "a")
        writer = csv.writer(f)
        writer.writerow([str(cpu)])
        f.close()

        perfTest(net)


def perfTest(net):
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing bandwidth between h1 and h4")
    cli1, cli2, serv1, serv2 = net.get('cli1', 'cli2', 'serv1', 'serv2')
    hosts = []
    hosts.extend([cli1,cli2,serv1, serv2])
    for i in range(3):
        result = hosts[i].cmd("ifconfig -a | grep 'ether' | awk ' {print $2}'")
        print("MAC address of host " + str(hosts[i]) + ": " + result)

    cli1.popen('chromedriver')

    serv1.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/peerjs-server')

    serv1.cmd('nohup peerjs --host 10.0.0.3 --port 3001 --key peerjs --path / &')

    serv2.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/webrtc-peer-socket-server')

    serv2.cmd('nohup npm run devStartSocket </dev/null &')

    time.sleep(10)

    p1 = cli1.popen('google-chrome --no-sandbox --remote-debugging-port=9222')
    cli1.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/webrtc-peer')
    cli1.cmd('nohup npm run devStart </dev/null &')

    time.sleep(10)

    cli2.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/webrtc-peer-2')
    cli2.cmd('nohup npm run devStart </dev/null &')

    time.sleep(10)

    cli1.cmd('cd ../../../../../../home/mininet/Workspace/datagrams-test/webrtc/webrtc')
    thread1 = cli1.popen('sudo python test-threading1.py')
    time.sleep(10)
    thread2 = cli1.popen('sudo python test-threading2.py')

    time.sleep(30)

    poll1 = thread1.poll()

    while (poll1 is None):
        poll1 = thread1.poll()

    print("poll1 is complete")

    time.sleep(5)

    net.stop()

    thread1.terminate()
    thread2.terminate()

    p1.terminate()

    with open('results.csv','r') as f:
        data = [] 
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

        lastRows = data[-2:] 
        flat_list = []
        for sublist in lastRows:
            for item in sublist:
                if ',' in item:
                    item = item.split(',')
                    flat_list.extend(item)
                else:
                    flat_list.append(item)

        data = data[:-2]

        data.append(flat_list)
            
    with open('results.csv','w') as f: 
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)

    # CLI(net)
    time.sleep(10)

if __name__ == '__main__':
    setLogLevel('info')
    start()


