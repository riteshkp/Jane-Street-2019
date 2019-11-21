#!/usr/bin/env python3
# coding: utf8

"""
tcp_connect.py
Date: 11-09-2019

Description: Trading bot strategy for Ornus for Jane Street ETC
Authors:
    Apostolos Delis
    Gary Vartanian
    Ritesh Pendekanti
"""

import sys
import socket
import json
import time
from collections import defaultdict

import strategies
from constants import *



# ~~~~~============== NETWORKING CODE ==============~~~~~
class TCPConnect:
    def __init__(self):
        self.server_status = server_status
        self.data = defaultdict(lambda: list())
        self.exchange = None
        self.order_id = 0

    def connect(self):
        print("Initializing connection to server...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Initialized")
        s.connect((exchange_hostname, port))
        print("Connected successfuly to server...")
        self.server_status = SUCCESSFUL_CONNECTION
        self.exchange = s.makefile('rw', 1)

    def write_to_exchange(self, obj: dict):
        try:
            obj["order_id"]
            self.order_id += 1
        except KeyError:
            pass

        json.dump(obj, self.exchange)
        # print("Writing to exchange...")
        self.exchange.write("\n")

    def read_from_exchange(self):
        # print("Reading exchange...")
        return json.loads(self.exchange.readline())

    def get_data(self):
        # global server_status
        count = 0
        print("Updating Server info...")
        while(count < 500):
            try:
                info = self.read_from_exchange()
            except:
                continue
            if not info:
                break
            type = info["type"]
            if(info["type"] == "close"):
                # server_status = 0;
                self.server_status = NO_CONNECTION
                print("Server closed.")
                return
            if(info["type"] == "trade"):
                self.data[info["symbol"]].append(info["price"])
            time.sleep(0.01)
            count += 1

    def reconnect(self):
        print("\nMarket Closed. Reconnecting...\n")
        while(self.server_status == NO_CONNECTION):
            try:
                print("Reconnect: restablishing TCP connect")
                self.connect()
                self.write_to_exchange({"type": "hello",
                                        "team": TEAM_NAME.upper()})
                hello_from_exchange = self.read_from_exchange()
                print("Reconnect: message received:", hello_from_exchange)
                if(hello_from_exchange["type"] == "hello"):
                    self.server_status = SUCCESSFUL_CONNECTION
                    print("----------------Handshake Success!----------------")
                else:
                    self.server_status = NO_CONNECTION
                    print("----------------Handshake Error!----------------")
            except socket.error:
                 print("\r\nReconnect: socket error, do reconnect ")
                 time.sleep(0.1)

    def action(self):
        valbz = self.data["VALBZ"][-WINDOW_SIZE:]
        vale = self.data["VALE"][-WINDOW_SIZE:]
        bond = self.data["BOND"][-WINDOW_SIZE:]
        wfc = self.data["WFC"][-WINDOW_SIZE:]
        gs = self.data["GS"][-WINDOW_SIZE:]
        ms = self.data["MS"][-WINDOW_SIZE:]
        xlf = self.data["XLF"][-WINDOW_SIZE:]

        strategies.bond_strategy(self, bond, self.order_id)
        strategies.valbz_vale(self, valbz, vale, self.order_id)
        strategies.xlf_strat(self, xlf, bond, gs, ms, wfc, self.order_id)

# ~~~~~============== MAIN LOOP ==============~~~~~
def main():
    exchange = TCPConnect()
    exchange.connect()
    exchange.write_to_exchange({"type": "hello", "team": TEAM_NAME.upper()})
    hello_from_exchange = exchange.read_from_exchange()
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

    i = 0
    while(True):
        i += 1
        print("Iteration:", i)
        exchange.get_data()
        if (exchange.server_status == SUCCESSFUL_CONNECTION):
            exchange.action()
        else:
            exchange.reconnect()


def initialize():
    print("Initializing Trading Bot...")
    print("\tTest Mode:", test_mode)
    print("\tPort:", port)
    print("\tHostname:", exchange_hostname)


if __name__ == "__main__":
    initialize()
    while True:
         try:
             main()
         except socket.error:
             print("\nMain: socket error, do reconnect")
             time.sleep(0.1)
