#! coding: utf-8

import os
import logging

#from netmiko import ConnectHandler

class ConnectionHandler():
    def send_command(self, cmd):
        print("executing command: %s" % cmd)

        return "\nfinished the command: %s\n" % cmd

def init_connector(netype, host):
    return ConnectionHandler()

class Collector(object):
    """
    """
    def __init__(self, netype, host):
        self.netype = netype
        self.host = host
        self.conn = init_connector(netype, host)

    def get_cmd_list(self, checkitem_list):
        cmdlist = [item.check_cmd for item in checkitem_list]
        return cmdlist

    def run(self, host, cmdlist):
        output_buf = []

        for cmd in cmdlist:
            print("executing '%s' on '%s'" % (cmd, self.host))
            output = self.conn.send_command(cmd)
            output_buf.append("\n=== %s ===" % cmd.strip())
            output_buf.append(output)
        
        self.logbuf = output_buf
        print("".join(output_buf))
        return output_buf
        