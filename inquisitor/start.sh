#!/bin/bash
echo "Waiting for the containers to start..."
docker-compose up -d
echo "Inspect the network and list the running containers... "
docker container ls
echo "Network inspect..."
docker network inspect inquisitor_network_inquisitor | grep -e MacAddress -e Name -e IPv4
echo "Connect to SSH:\n ssh -p 8484 root@localhost \n password: root"