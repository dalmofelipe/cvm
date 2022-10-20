#!/bin/bash

systemctl start docker docker.socket containerd

sleep 2

docker ps