#   Guide Docker


# Path: inquisitor/README.md
docker network ls
docker network inspect inquisitor_default
docker exec -it attacker bash
docker exec -it client-ftp bash
docker exec -it server-ftp bash
python3 inquisitor.py 172.26.0.3 02:42:ac:12:00:03 172.26.0.4 02:42:ac:12:00:04 -v