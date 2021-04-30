import time
import subprocess
import mysql.connector

#Datenbankverbindung herstellen
mydb = mysql.connector.connect( 
    host="10.0.0.3",
    user="******",
    password="*******",
    database="monicont",
)
mycursor = mydb.cursor(buffered=True)

hostname = subprocess.check_output("hostname", shell=True).decode('utf-8').replace('-','_').strip() #Auslesen des Hostnames
ip = subprocess.check_output("ip addr | grep inet | grep eth0 | awk '{print $2}'", shell=True).decode('utf-8').strip()#Auslesen der IP Adresse

mycursor.execute("Insert INTO MainMonitoring (name, ip) VALUES ('"+str(hostname)+"','"+str(ip)+"') ON DUPLICATE KEY UPDATE `ip` = '"+str(ip)+"';") #Name und IP in die Übersichtstabelle einfügen
mydb.commit() #Datenbank Commit

try:
    mycursor.execute("Select * FROM "+hostname+" Limit 1;") #prüfen ob breits eine Tabelle vorhanden
except: #Keine Tabelle vorhanden -> Neue Tabelle anlegen
    mycursor.execute("CREATE TABLE "+hostname+" (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(100), `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, `uptime` varchar(100) DEFAULT NULL, `cpu` float DEFAULT NULL, `ram` float DEFAULT NULL, `swap` float DEFAULT NULL, `processes` int DEFAULT NULL, `apache_err` int DEFAULT NULL, `apache_acc` int DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")

while True:
    cpu = subprocess.check_output("sar 1 1 | grep -i -v Linux | awk 'NF' | grep -i -v Durchschnitt | grep -i -v % | awk '{print $8}' | head -1", shell=True).decode('utf-8') #Lese CPU Anteil im Ruhestand in %
    cpu = 100 - float(cpu) #Konvertiere von Anteil Ruhezustand zu Anteil Auslastung
    cpu = round(cpu, 2) #Runde auf zwei Nachkommerstellen

    ram = subprocess.check_output("free | grep -i 'Mem' | awk '{print $3}'", shell=True).decode('utf-8') #Lese Ram Auslastung
    ram = float(ram) / 1024 #Konvertiere von KiBi in MiBi
    ram = round(ram, 2) #Runde auf zwei Nachkommerstellen

    swap = subprocess.check_output("free | grep -i 'Swap' | awk '{print $3}'", shell=True).decode('utf-8') #Lese die Swap Auslastung
    swap = float(swap) / 1024 #Konvertiere von KiBi in MiBi
    swap = round(swap, 2) #Runde auf zwei Nachkommerstellen   

    processes = subprocess.check_output("ps -aux | wc -l", shell=True).decode('utf-8') #Lese die Anzahl der laufenden Prozesse

    uptime = subprocess.check_output("uptime | awk '{print $3}'", shell=True).decode('utf-8').strip().replace(',','') #Lese die Uptime
    
    mycursor.execute("INSERT INTO "+hostname+" (name, cpu, ram, swap, processes, uptime) VALUES ('"+str(hostname)+"',"+str(cpu)+","+str(ram)+","+str(swap)+","+processes+",'"+str(uptime)+"');") #Füge die Werte in die Datenbank
    mydb.commit() #Datenbank Commit
    time.sleep(30) #Warte 30 Sekunden
