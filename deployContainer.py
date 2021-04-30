import os

i = 0
while i < 6: #i = wie viele Container werden erstellt
    command = "lxc launch ubuntu:20.04 -p macvlan" #erstelle einen Container mit Ubuntu:20.04 und macvlan profil
    os.system(command) # Komanndo ausführen
    i = i + 1
