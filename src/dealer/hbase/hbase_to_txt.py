#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
import happybase


def to_hbase():
    connection = happybase.Connection('localhost', autoconnect=False)
    connection.open()
    table = connection.table('testtable')
    for key, data in table.scan():
        print(key.decode("utf-8"), data.decode("utf-8"))
        break

to_hbase()