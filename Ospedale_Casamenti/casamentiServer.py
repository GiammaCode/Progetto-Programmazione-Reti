'''
    Elaborato Programmazione di Reti
            a.a. 2020/2021
           Casamenti Gianmaria
           Matricola: 0000925151
               Traccia 2
'''
#!/bin/env python
import sys, signal
import http.server
import socketserver
#new imports
import threading 


#gestisce l'attesa evitando busy waiting
waiting_refresh = threading.Event()

# Legge il numero della porta da riga di comando, e mette di default 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
  
                
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

# la parte iniziale è identica per tutti i servizi
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {text-align:justify;}
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: #333;
  		    }
            .topnav a {
  		        float: left;
  		        color: #f2f2f2;
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: #ddd;
  		        color: tomato;
  		    }        
  		    .topnav a.active {
  		        background-color: #4CAF50;
  		        color: lightGray ;
  		    }
        </style>
    </head>
    <body>
        <title>Ospedale Casamenti</title>
"""

# la barra di navigazione servizi
navigation_bar = """
        <br>
        <br>
        <br>
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}">Home</a>
  		    <a href="http://127.0.0.1:{port}/servizio_118.html">Emergenza 118</a>
            <a href="http://127.0.0.1:{port}/pronto_soccorso.html">Pronto soccorso</a>
            <a href="http://127.0.0.1:{port}/guardia_medica.html">Guardia medica</a>
            <a href="http://127.0.0.1:{port}/farmacie_di_turno.html">Farmacie di turno</a>
            <a href="http://127.0.0.1:{port}/formazione_tirocinio.html">Formazione tirocinio</a>
            <a href="http://127.0.0.1:{port}/FSE.html">FSE - fascicolo sanitario elettronico</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">Aggiorna</a>
            <a href="http://127.0.0.1:{port}/Relazione_casamenti.pdf" download="Relazione_casamenti.pdf" style="float: right">Download info pdf</a>
            <a href="http://127.0.0.1:{port}/accedi_servizi.html" style="float: right">Accedi</a>
  		</div>
        <br><br>
        <table align="center">
""".format(port=port)

# la parte finale uguale per tutti i servizi
footer_html= """
        </table>
    </body>
</html>
"""

#la parte finale per la pagine principale dove è possibile accedere al FSE
end_page_accedi = """
        <br><br>
		<form action="https://www.auslromagna.it/servizi-on-line/fse-fascicolo-sanitario-elettronico" target="_blank" style="text-align: center;">
		  <h1><strong>IL MIO Fascicolo Sanitario Elettronico</strong></h1><br>
          <h1><strong>Inserisci UserName e password per accedere al tuo FSE</strong></h1><br>
          <input type="text" name="username" value="username" ><br><br>
          <input type="text" name="password" value="pwd" ><br><br>
          <input type="submit" value="ACCEDI" ><br><br>
          <a href="https://www.auslromagna.it/servizi-on-line/fse-fascicolo-sanitario-elettronico"><h1>Iscriviti per creare il tuo FSE</h1></a>
          </form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina home
end_page_index = """
        <br><br>
		<form action="http://127.0.0.1:{port}/home" method="post" style="text-align: center;">
		  <h1><strong>AZIENDA SANITARIA CASAMENTI</strong></h1><br>
          <h1>L'Azienda Unita' Sanitaria Locale, istituita con Legge regionale n. 22 del 21 novembre 2013,</h1><br>
          <h1>e' l'ente strumentale attraverso il quale la Regione assicura i livelli essenziali ed uniformi</h1><br>
          <h1>di assistenza dell'ambito territoriale della Romagna.</h1><br>
          <img src='images/homepage.gif'/>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina emergenza 118
end_page_servizio_118 = """
        <br><br>
		<form action="http://127.0.0.1:{port}/servizio_118" method="post" style="text-align: center;">
          <img src='images/logo118.png'/ width="100" height="100">
          <h1><strong>EMERGENZA 118</strong></h1><br>
          <h1>In caso di incidente, infortunio, di grave problema e necessita' urgente di soccorso,</h1><br>
          <h1> chiamate il 118 per ottenere l'intervento immediato dei servizi di emergenza.</h1><br>
          <h1>La chiamata e' gratuita.</h1><br>
          <a href="https://www.118er.it/"><h1>Ulteriori informazioni sul 118.</h1></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina pronto soccorso
end_page_pronto_soccorso= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso" method="post" style="text-align: center;">
		  <img src='images/pronto_soccorso.png'/ width="100" height="100">
          <h1><strong>PRONTO SOCCORSO e PRONTO INTERVENTO</strong></h1><br>
          <h1>Il servizio di Pronto Soccorso e' rivolto a persone che hanno di bisogno di cure urgenti.</h1><br>
          <h1> Per situazioni non urgenti e' opportuno rivolgersi direttamente al proprio medico di famiglia od</h1><br>
          <h1>al servizio sostitutivo di guardia medica.</h1><br>
          <a href="https://www.auslromagna.it/luoghi/pronto-soccorso"><h1>Trova il pronto soccorso piu' vicino</h1></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina guardia medica
end_page_guardia_medica= """
        <br><br>
		<form action="http://127.0.0.1:{port}/guardia_medica" method="post" style="text-align: center;">
		   <img src='images/guardia_medica.png'/ width="100" height="100">
          <h1><strong>CONTINUITA' ASSISTENZALE</strong></h1><br>
          <h1>(Guardia medica)</h1><br>
          <h1>Si tratta di un servizio di guardia medica che prosegue l'attivita' del Medico di Famiglia </h1><br>
          <h1>nei giorni e orari in cui queste figure non sono presenti.</h1><br>
          <a href="https://www.auslromagna.it/servizi/guardia-medica"><h1>Trova il numero telefonico del comprensorio</h1></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina farmacie di turno
end_page_farmacie_di_turno= """
        <br><br>
		<form action="http://127.0.0.1:{port}/farmacie_di_turno" method="post" style="text-align: center;">
		  <img src='images/farmacie_di_turno.png'/ width="100" height="100">
          <h1><strong>FARMACIE DI TURNO</strong></h1><br>
          <h1>Il servizio di farmacie di turno e' rivolto a persone che necessitano</h1><br>
          <h1>di farmacie aperte in orari non lavorativi</h1><br>
          <a href="https://www.auslromagna.it/servizi/farmacie"><h1>Trova la famacia di turno</h1></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina formazione tirocinio
end_page_formazione_tirocinio= """
        <br><br>
		<form action="http://127.0.0.1:{port}/formazione_tirocinio" method="post" style="text-align: center;">
		  <h1><strong>FORMAZIONE E TIROCINIO</strong></h1><br>
          <h1>La formazione continua e' uno degli strumenti fondamentali per garantire nel tempo</h1><br>
          <h1>le prestazioni del Servizio Sanitario.</h1><br>
          <a href="https://www.auslromagna.it/cura/universita"><h1>Informazioni Universitarie </h1></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina FSE
end_page_FSE= """
        <br><br>
		<form action="http://127.0.0.1:{port}/FSE" method="post" style="text-align: center;">
		  <img src='images/fse.png'/ width="100" height="100">
          <h1><strong>FASCICOLO SANITARIO ELETTRONICO</strong></h1><br>
          <h1>Il Fascicolo Sanitario Elettronico (FSE) consente l'archiviazione e la consultazione </h1><br>
          <h1>da pc e da smartphone dei propri dati e documenti di tipo sanitario e socio-sanitario,</h1><br>
            <h1><strong>in forma riservata e protetta.</strong></h1><br>
          <a href="accedi_servizi.html"><h1>accedi al tuo FSE</h1></a>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

# creo tutti i file utili per navigare.
def resfresh_contents():
    print("updating all contents")
    create_page_servizio_118()
    create_page_pronto_soccorso()
    create_page_guardia_medica()
    create_farmacie_di_turno()
    create_page_formazione_tirocinio()
    create_page_FSE()
    create_index_page()
    print("finished update")

# creazione della pagina specifica del servizio Accedi    
def create_page_accedi_servizi():
    f = open('accedi_servizi.html','w', encoding="utf-8")
    f.write(header_html + " <br><br><h1>Accedi</h1> " + navigation_bar + "</table>" + end_page_accedi)
    f.close()

# creazione della pagina specifica del servizio 118
def create_page_servizio_118():
    create_page_servizio("<h1>Emergenza 118</h1>"  , 'servizio_118.html', end_page_servizio_118 )

# creazione della pagina specifica del pronto soccorso
def create_page_pronto_soccorso():
    create_page_servizio("<h1>Pronto soccorso</h1>"  , 'pronto_soccorso.html', end_page_pronto_soccorso )

# creazione della pagina specifica dell guardia medica
def create_page_guardia_medica():
    create_page_servizio("<h1>Guardia medica</h1>"  , 'guardia_medica.html', end_page_guardia_medica )

# creazione della pagina specifica per le farmacie di turno
def create_farmacie_di_turno():
    create_page_servizio("<h1>Farmacie di turno</h1>" , 'farmacie_di_turno.html', end_page_farmacie_di_turno )
    
# creazione della pagina specifica fotmazione e tirocini
def create_page_formazione_tirocinio():
    create_page_servizio("<h1>Formazione e tirocinio</h1>" , 'formazione_tirocinio.html', end_page_formazione_tirocinio )

# creazione della pagina specifica del FSE
def create_page_FSE():
    create_page_servizio("<h1>FSE - Fascicolo sanitario elettronico</h1>", 'FSE.html', end_page_FSE )
    
# creazione della pagina index.html (iniziale)
# contenente pagina principale del Azienda ospedaliera
def create_index_page():
    create_page_servizio("<h1>Elaborato Casamenti</h1>", 'index.html', end_page_index )
    
#metodo lanciato per la creazione delle pagine servizi
def create_page_servizio(title,file_html, end_page):
    f = open(file_html,'w', encoding="utf-8")
    try:
        message = header_html + title + navigation_bar + end_page
        message = message + footer_html
    except:
        pass
    f.write(message)
    f.close()

# Lancio un thread che aggiorna ogni 5 minuti i 
# contenuti delle pagine     
def launch_thread_resfresh():
    t_refresh = threading.Thread(target=resfresh_contents())
    t_refresh.daemon = True
    t_refresh.start()
    
# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
      
# metodo che viene chiamato al "lancio" del server
def main(): 
    usr = input("inserire username: ")
    pwd = input("inserire password: ")
    if usr == 'admin' and pwd == 'admin' : 
        # lancio un thread che aggiorna ricorrentemente i servizi
        launch_thread_resfresh()
        #Assicura che da tastiera usando la combinazione
        #di tasti Ctrl-C termini in modo pulito tutti i thread generati
        server.daemon_threads = True 
        #il Server acconsente al riutilizzo del socket anche se ancora non è stato
        #rilasciato quello precedente, andandolo a sovrascrivere
        server.allow_reuse_address = True  
        #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
        signal.signal(signal.SIGINT, signal_handler)
        #creo pagina accedi ai tuoi servizi
        create_page_accedi_servizi()
        # cancella i dati get ogni volta che il server viene attivato
        f = open('AllRequestsGET.txt','w', encoding="utf-8")
        f.close()
        # entra nel loop infinito
    else:
        print("ACCESSO NEGATO")
      
    try:
            while True:
                server.serve_forever()
    except KeyboardInterrupt:
      pass
      server.server_close()
        

if __name__ == "__main__":
    main()
