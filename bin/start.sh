#!/bin/bash
nohup crawler-scheduler > scheduler.log 2>&1 &
nohup crawler-worker > worker.log 2>&1 &