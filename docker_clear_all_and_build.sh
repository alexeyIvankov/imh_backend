#!/bin/bash

echo "Starting clear all container and images"
sleep 3

sudo service docker start
sudo docker-compose stop
sudo docker system prune
sudo docker rmi -f $(sudo docker images)
sudo docker volume rm $(sudo docker volume ls)
sudo service docker restart
sleep 1
sudo git pull
sudo docker-compose up --build

