#!/bin/bash

for i in `ps -ef | grep python | grep -E 'crawler-scheduler' | awk '{print $2}'`
do
  echo 'check pid: '${i}
  if [[ `pwdx ${i} | grep -c test_crawler` -eq '1' ]]; then
      echo 'kill pid: '${i}
      kill ${i}
  fi
done