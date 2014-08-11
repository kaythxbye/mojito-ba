#!/usr/bin/env python2

from optparse import OptionParser
import subprocess, time

def execute_on_host(hostname, call_string):
    try:
        retval = subprocess.check_output("../../oldrepo/mininet/util/m " + str(hostname) + " " + str(call_string), shell=True)
    except subprocess.CalledProcessError:
        print "Error with command " + str(call_string) + " on host " + str(hostname) + "."
        retval = ""
    return retval

# add default entry in routing table of receiver
def set_routing_table():
    execute_on_host("h2", "route add default gw 10.0.0.1 h2-eth0")

def run_sender(tracefile):
    execute_on_host("h1", "/home/samuel/studium/ba/mojito/eval/sender /home/samuel/studium/ba/mojito/eval/" + str(tracefile) + " no" + " no")

def get_netstat(host):
    netstat_output = execute_on_host(host, "netstat -s -u")
#    print netstat_output
    lines = netstat_output.split("\n")
    for line in lines:
        if line.find("packets to unknown port received") != -1:
            return line.strip().split(" ")[0]
    return 0

def insert_rules_in_switch(ruleset):
    ruleset = ruleset[:-12]
    print "Ruleset = " + ruleset
    process = subprocess.Popen("./ruleset_to_trace.py -c b -i" + ruleset, shell=True)
    process.wait()

def start_mininet():
    devnull = open('/dev/null', 'w')
    subprocess.Popen("mn --topo single,2 --mac --switch user --controller remote", stdout=devnull, stderr=devnull, shell=True)
    time.sleep(3)

def stop_mininet():
    devnull = open('/dev/null', 'w')
    process = subprocess.Popen("mn -c", stdout=devnull, stderr=devnull, shell=True)
    process.wait()
    print "Mininet stopped."

def main():
    #parse options
    parser = OptionParser()
    parser.add_option("-t", "--trace-file", dest = "tracefile", default = "rulesets/2_100_0.random.rules.bcase_trace",
                      help = "input rule file (relative path from here)", metavar = "FILE")
    parser.add_option("-a", "--algorithm", dest = "algorithm", default = "list", 
                      help = "textual description of algorithm used", metavar = "NAME")

    (options, args) = parser.parse_args()
    tracefile = options.tracefile
    algorithm = options.algorithm

    times = []
    packets = []

    for run in range(0, 10):
        start_mininet()
        print "Started mininet"
        insert_rules_in_switch(tracefile)
        set_routing_table()
        
        old_udp_count = int(get_netstat("h2"))
        start = time.time()
        run_sender(tracefile)
        duration = time.time() - start
        print "Time to send trace: " + str(duration)
        times.append(duration)
        print "Packets received: " + str(int(get_netstat("h2")) - old_udp_count)
        packets.append(int(get_netstat("h2")) - old_udp_count)
        stop_mininet()

    time_string = ""
    for time_ in times:
        time_string += str(time_) + " "
    packet_string = ""
    for packet in packets:
        packet_string += str(packet) + " "
    print "Times: " + time_string
    print "Packets " + packet_string

if __name__ == '__main__':
    main()
