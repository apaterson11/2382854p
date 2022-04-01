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
import csv
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
        self.addLink(cli1, cli_switch)
        self.addLink(cli2, cli_switch)
        self.addLink(serv, serv_switch)
        self.addLink(cli_switch, serv_switch)
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

def stopServer(net):
    serv = net.get('serv')
    serv.stop()
    print("server stopped")


"Create network and run simple performance test"
def start():
    # bw_list = [100,90,80,70,60,50,40,30,20,10,1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
    # bw_list = [100,90,80,10,1]
    bw_list = [100, 10]
    for bw in bw_list:
        net = Mininet(DumbellTopo(), link=TCLink, controller=DefaultController)
        nodes = net.switches + net.hosts
        net.start()
        for node in nodes:
            changeBandwidth(node, bw)

        f = open("results.csv", "a")
        writer = csv.writer(f)
        writer.writerow([str(bw)])
        f.close()

        perfTest(net, bw)


def perfTest(net, new_bw):
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing bandwidth between h1 and h4")
    cli1, cli2, serv = net.get('cli1', 'cli2', 'serv')
    # serv.setIP('web-platform.test/24')
    hosts = []
    hosts.extend([cli1,cli2,serv])
    for i in range(3):
        result = hosts[i].cmd("ifconfig -a | grep 'ether' | awk ' {print $2}'")
        print("MAC address of host " + str(hosts[i]) + ": " + result)

    # cli1.popen('google-chrome http://localhost:4000  --remote-debugging-port=9222 --origin-to-force-quic-on=web-platform.test:0 --ignore-certificate-errors-spki-list=Che1LMoCaGGzz64nnim12yh7fKd4bGy6L2b9IHGeS/k= --no-sandbox')    


    # cli1.popen('google-chrome --no-sandbox')
    cli1.popen('chromedriver')
    p1 = cli1.popen('google-chrome --remote-debugging-port=9222 --origin-to-force-quic-on=web-platform.test:0 --ignore-certificate-errors-spki-list=Che1LMoCaGGzz64nnim12yh7fKd4bGy6L2b9IHGeS/k= --no-sandbox')

    time.sleep(10)

    serv.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/wpt')

    serv.cmd('nohup python wpt serve --webtransport-h3 &')

    time.sleep(10)

    cli1.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/webtransport-refactor-streams')
    cli1.cmd('nohup npm run devStart </dev/null &')

    filename = str(new_bw) + 'bw_capture_file.pcap'
    # p3 = cli1.popen('tcpdump src web-platform.test and dst 10.0.0.1 -c 1100 -w ' + filename)

    time.sleep(10)

    cli2.cmd('cd ../../../../../../../media/sf_l4-project-quic/builds/webtransport-refactor-streams-2')
    cli2.cmd('nohup npm run devStart </dev/null &')

    time.sleep(30)

    cli1.cmd('cd ../../../../../../home/mininet/Workspace/datagrams-test/tests')
    thread1 = cli1.popen('python test-threading1-streams.py')
    time.sleep(10)
    thread2 = cli1.popen('python test-threading2-streams.py')

    time.sleep(30)

    poll1 = thread2.poll()
    poll2 = thread1.poll()
    while (poll1 is None):
        poll1 = thread2.poll()

    print("poll1 is complete")

    time.sleep(5)

    net.stop()
    # switches = net.switches
    # for switch in switches:
    #     switch.stop()

    while (poll2 is None):
        poll2 = thread1.poll()

    p1.terminate()
    thread1.terminate()
    thread2.terminate()

    # parse output

    with open('results.csv','r') as f:
        data = [] 
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

        lastRows = data[-3:] 

        client_timestamps = lastRows[1][0].split(',')
        server_timestamps = lastRows[2]

        received_timestamps = server_timestamps[0].split(',')
        displayed_timestamps = server_timestamps[1].split(',')

        actual_latencies = []
        perceived_latencies = []

        for i in range(len(displayed_timestamps)):
            actual_latencies.append((int(received_timestamps[i]) - int(client_timestamps[i]))) 
            perceived_latencies.append((int(displayed_timestamps[i]) - int(client_timestamps[i]))) 

        actual_latency = sum(actual_latencies) / len(actual_latencies)
        perceived_latency = sum(perceived_latencies) / len(perceived_latencies)

        flat_list = []

        flat_list.append(lastRows[0][0])
        flat_list.append(actual_latency/1000)
        flat_list.append(perceived_latency/1000)

        data = data[:-3]

        data.append(flat_list)
            
    with open('results.csv','w') as f: 
        writer = csv.writer(f)
        writer.writerows(data)

    # cli1.cmd('mv *.pcap ../../../../../media/sf_l4-project-quic/builds/webtransport-refactor-datagrams/logs/bandwidth')

    # CLI(net)
    time.sleep(20)

if __name__ == '__main__':
    setLogLevel('info')
    start()


