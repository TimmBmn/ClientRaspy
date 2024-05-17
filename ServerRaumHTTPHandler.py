# Webserver für die Serverraumüberwachung
# Zugriff auf die Web - Seite:  server:1111
# zugriff auf die Ajax java Scrip Datei: server:1111/data_request.js
# zugriff auf die CSS Datei: server:1111/style.css
# Abfrage der Sensordaten: server:1111/data (sendet JSON Daten für Raumnummer, Temperatur und Feuchtigkeit)
#
# Der Server implementiert nur HTTP GET, wer irgendwas über POST oder PUSH schicken will -> have fun!!

import socketserver
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from typing import Tuple


class ServerRaumHTTPHandler(BaseHTTPRequestHandler):
    # die Variablen sind static, weil für jeden GET Request eine neue Instanz des ServerRaumHTTPServer
    # erzeugt wird und der SensorClient nicht an die Objektmember herankommt
    room = 200 
    temp = 0
    water = 0
    tlimit = 0


    # Initialisierung des Servers
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        # Aufruf des Basiklassen  Pseudo - Konstruktor, also der __init __ Methode
        super().__init__(request, client_address, server)
        # debug - Ausgabe, im Betrieb entfernen
        print(self.path)
        print(self.server)

    def do_GET(self):
        if self.path == "/":
            # Webseite schicken
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            file = open("index.html", "rb")
            seite = file.read()
            self.wfile.write(seite)

        if self.path == "/data_request.js":
            # JavaScript Datei schicken
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            file = open("data_request.js", "rb")
            js = file.read()
            self.wfile.write(js)

        if self.path == "/style.css":
            # css Datei schicken
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            file = open("style.css", "rb")
            cs = file.read()
            self.wfile.write(cs)

        if self.path == "/data":
            # senden der Daten als JSON
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            data = json.dumps(
                    {   "room"  : str(ServerRaumHTTPHandler.room),
                        "temp"  : ServerRaumHTTPHandler.temp,
                        "water" : ServerRaumHTTPHandler.water,
                        "tlimit": ServerRaumHTTPHandler.tlimit
                    })

            self.wfile.write(bytes(data, "utf-8"))

    # run ist statisch!!
    @staticmethod
    def run(hostName, serverPort):
        webserver = HTTPServer((hostName, serverPort), ServerRaumHTTPHandler)
        t = threading.Thread(target=webserver.serve_forever, daemon=True)
        t.start()
        print("Webserver started http://%s:%s" % (hostName, serverPort))


# Der Code bleibt nur hier, damit man den Server testweise auch standalone starten kann
# normalerweise wird der HTTTP Server vom SensorClient instanziert

if __name__ == "__main__":
    testserver = HTTPServer(("localhost", 1111), ServerRaumHTTPHandler)
    t = threading.Thread(target=testserver.serve_forever, daemon=True)
    t.start()
    print("Testserver started http://%s:%s" % ("localhost", "1111"))
    while True:
        time.sleep(1)
