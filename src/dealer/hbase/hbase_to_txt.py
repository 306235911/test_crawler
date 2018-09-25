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
        jdata = json.loads(data[b'cf1:'].decode(encoding='utf-8'))
        if "<h1 " in jdata['title']:
            table.delete(key)
            print("bad title del...")
        else:
            break

to_hbase()