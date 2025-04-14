## Name

Blind test

## Description

You've stumbled across a server that appears to be abandoned but protected by filters. Find a way to read the hidden secret.


## Difficulty

Easy

## Flag 
`MCTF{kIll3d_3xFi}`


## Solve

TL;DR : exfiltration d'un fichier avec filtre seccomp qui empêche de rev shell/exfiltrer et de write sur la sortie. Il faut donc se baser sur le kill du programme, voir script.

voir script.py :
```
python3 script.py 127.0.0.1 4444
```


