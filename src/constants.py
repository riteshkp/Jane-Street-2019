#!/usr/bin/env python3
# coding: utf8

"""
constants.py
Date: 11-09-2019

Description: Constants used for the competition
"""

SUCCESSFUL_CONNECTION = 1
NO_CONNECTION = 0
TEAM_NAME="Ornus"
test_mode = False
test_exchange_index=0   # 0 = prod-like, 1 = slower, 2 = empty
prod_exchange_hostname="production"
port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + TEAM_NAME if test_mode else prod_exchange_hostname
server_status = 1
WINDOW_SIZE = 25


if __name__ == "__main__":
    pass
