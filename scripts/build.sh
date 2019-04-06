#!/bin/bash
docker pull pklehre/niso2019-lab5
docker build -t niso5-sxc678 .
docker image prune -f