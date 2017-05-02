#!/bin/bash

docker run \
  -it \
  --rm \
  -v `pwd`/app:/usr/src/app \
  --name osqmanager \
  --net host \
  srozb/osqmanager \
  bash
