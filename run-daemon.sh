#!/bin/bash

docker run \
  -d \
  -v `pwd`/app:/usr/src/app \
  -v `pwd`/../db:/usr/src/app/osqmanager/db \
  --name osqmanager \
  --net host \
  srozb/osqmanager
