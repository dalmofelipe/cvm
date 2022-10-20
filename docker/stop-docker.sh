#!/bin/bash

systemctl stop docker docker.socket containerd

sleep 2

systemctl status docker docker.socket containerd