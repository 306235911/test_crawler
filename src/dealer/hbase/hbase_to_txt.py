#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import json

import happybase


def to_hbase():
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    table = connection.table('testtable')
    for key, data in table.scan():
        print(key.decode("utf-8"))
        print(json.loads(data))
        break

to_hbase()