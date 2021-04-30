import os
import subprocess

containerlist = []
containerlist = subprocess.check_output("lxc list | awk '{print $2}' | grep -i -v 'Name' | awk NF", shell=True).decode('utf-8').splitlines() #speichere alle Containernamen in einen Liste

for container in containerlist: #wende die folgdenen Befehle auf jeden Container in der Liste an
    print(container)
    os.system("lxc exec "+str(container)+" -- sudo apt update") #Systemupdate
    os.system("lxc exec "+str(container)+" -- sudo apt upgrade -y") #Systemupdate
    os.system("lxc exec "+str(container)+" -- sudo apt install sysstat python3-pip -y") #Installiere nötige Pakete
    os.system("lxc exec "+str(container)+" -- sudo pip3 install mysql-connector-python") #Installiere nögige Pakete

    try:
        os.system("lxc exec "+str(container)+" -- systemctl stop monitoring.service") #Wenn es den Service schon gibt, stoppe ihn
    except:
        pass
    os.system("lxc file push startMonitoring.sh "+str(container)+"/usr/local/bin/") #Kopiere das StartSkript vom Host in den Container
    os.system("lxc file push monitoring.py "+str(container)+"/usr/local/bin/") #Kopiere das Monitoring Porgramm vom Host in den Container

    try:
        output = subprocess.check_output("lxc exec "+str(container)+" -- [ ! -e /etc/systemd/system/monitoring.service ]; echo $?") #gibt es schon eine Autostart Konfiguration?
        if output == 0: #Datei nicht vorhanden
            print("Copy File")
            os.system("lxc exec "+str(container)+" -- systemctl stop monitoring.service") #Stoppe den Service, falls er laufen sollte
            os.system("lxc file push monitoring.service "+str(container)+"/etc/systemd/system/") #Kopiere die Konfiguration vom Host in den Container
            os.system("lxc exec "+str(container)+" -- systemctl enable monitoring.service") #Aktiviere den Autostart
            os.system("lxc exec "+str(container)+" -- systemctl start monitoring.service") #Starte den Service
        else:
            os.system("lxc exec "+str(container)+" -- systemctl enable monitoring.service") #Aktiviere den Autostart, falls nicht geschehen
            os.system("lxc exec "+str(container)+" -- systemctl start monitoring.service") #Start den Service, falls nicht geschen
    except: #Falls beim Prüfen der Datei Fehler auftrete, kopiere sie, aktiviere den Autostart und starte den Service
        print("Copy File")
        os.system("lxc exec "+str(container)+" -- systemctl stop monitoring.service")
        os.system("lxc file push monitoring.service "+str(container)+"/etc/systemd/system/")
        os.system("lxc exec "+str(container)+" -- systemctl enable monitoring.service")
        os.system("lxc exec "+str(container)+" -- systemctl start monitoring.service")


