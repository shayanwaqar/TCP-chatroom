# TCP-chatroom

This project implements a simple client-server chatroom using Python sockets. The server allows multiple clients to connect, send messages, and use predefined chat shortcuts. Messages are broadcasted to all connected clients, and private messages can be sent using the direct message (`:dm`) feature.


* The server listens for incoming connections and manages multiple clients using threads.
* Clients authenticate using a common passcode.
* Messages are handled and broadcasted to all clients, except private messages which are sent only to the intended recipient.
* Uses TCP sockets to maintain persistent connections.
* The server binds to `<span>127.0.0.1</span>`, so it runs locally.
* The passcode is case-sensitive and limited to 5 alphanumeric characters.
* Usernames are limited to 8 characters.
* Clients must use the `<span>:Exit</span>` command to leave the chatroom properly.


To start the server, run:

python3 server.py -start -port `<port>` -passcode `<passcode>`

e.g

python3 server.py -start -port 12345 -passcode hello

To connect a client to the server, run:

python3 client.py -join -host <server_ip> -port `<port>` -username `<username>` -passcode `<passcode>`

e.g

python3 client.py -join -host 127.0.0.1 -port 12345 -username Alice -passcode hello


## Features

* Clients can join the chatroom by providing a username and a passcode.
* Messages are broadcasted to all connected clients.
* Shortcuts:
  * `<span>:)</span>` → [Feeling Joyful]
  * `<span>:(</span>` → [Feeling Unhappy]
  * `<span>:mytime</span>` → Displays current time.
  * `<span>:+1hr</span>` → Displays time +1 hour.
  * `<span>:dm <username> <message></span>` → Sends a private message to a specific user.
  * `<span>:Exit</span>` → Disconnects from the server.
* The server logs all client activity.
