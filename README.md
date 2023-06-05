<h1 align="center">
📖 Inquisitor | 42 Cybersecurity Bootcamp
</h1>

<p align="center">
	<b><i>Containers, ARP and MiddleMan</i></b><br>
</p>

<p align="center">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/Falitomal/inquisitor?color=lightblue" />
	<img alt="Code language count" src="https://img.shields.io/github/languages/count/Falitomal/inquisitor?color=yellow" />
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/Falitomal/inquisitor?color=blue" />
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Falitomal/inquisitor?color=green" />
</p>

## ✏️ Summary
```
This project can be done using virtual images or by deploying Docker containers. In my case, I have performed the deployment using a Docker Compose configuration.

The way Docker Compose works is as follows:

An "ftp-client" container is deployed whose communications will be intercepted.
A "server-ftp" container is deployed whose communications will also be intercepted.
A Dockerfile image is generated for the "attacker" container, which will be the container that performs the MiddleMan attack.
Each container will contain a shared volume on the local machine, into which the files will be downloaded.
The "attacker" container will install libraries using libcap and intercept the packages. To do this, services such as SSH, network utilities and ping utils will be installed. In addition, Python3 and the necessary network libraries will be installed, as well as other useful libraries such as argparse, request and pcapy.

```
## 💡 About the project

```

Inquisitor is a program with the following features:

It takes four parameters as inputs.
It performs ARP poisoning in both directions, allowing for full duplex communication interception.
When the attack is stopped using the CTRL+C command, the ARP tables are automatically restored to their original state.
The program exclusively works with IPv4 addresses.
It intercepts the traffic generated during the login process to an FTP server.
The program displays the names of the files exchanged between the client and the FTP server in real time.
It is designed to handle all possible input errors and ensures that the program never terminates unexpectedly.

```

## 🛠️ Usage

The program will be executed using the following command:

```
python3 inquisitor.py <ip-ftp-client> <mac-ftp-client> <ip-ftp-server> <mac-ftp-server> -v
```
You can also run the program using the following command:

```
python3 inquisitor.py
```

The program only works with IP addresses in IPV4 format and not with IPV6.
It will run in real time, without saving the results to a file.
You can use the -v parameter to see the packets being sent.
The -h parameter can be used to view the program's help.

The bonus part, which is the verbose option, is implemented and is executed using the -v parameter, but in the evaluation it is ignored.

Please note that this text is a general description based on the information provided, and I cannot review the specific functionality of the code without more details.


##  🛠️ Useful commands

```
docker network ls

docker network inspect inquisitor_default

docker exec -it attacker bash

docker exec -it client-ftp bash

docker exec -it server-ftp bash

python3 inquisitor.py 172.26.0.3 02:42:ac:12:00:03 172.26.0.4 02:42:ac:12:00:04 -v
```
