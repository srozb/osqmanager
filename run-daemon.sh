#!/bin/bash

docker run \
  -d \
  -v `pwd`/app:/usr/src/app \
  --name osqmanager \
  --net host \
  srozb/osqmanager
