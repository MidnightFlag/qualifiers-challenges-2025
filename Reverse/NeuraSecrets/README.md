# Setup

## Server
### Configuration
Change shellcodes/*.ma urls from `<URL>:<PORT>` to your public server
Change the `<PORT>` by your desired port

### Start
```sh
docker build -t neurasecrets_server .
docker run --name neurasecrets-server -d -p <PORT>:10000 neurasecrets_server

# get the flag encrypted
docker cp 
```

## Agent

### Configuration
Change in main.go : `<URL>:<PORT>` to your public server 

### Build
Build with go >=1.23
```sh
go build -ldflags="-s -w" -o neurasecrets .
```

# Description CTFd

NeuraTek released a new way to protect files : NeuraTek.
Try to find what this mysterious file contains

## Chall files

- NeuraSecrets elf
- flag.txt.enc

