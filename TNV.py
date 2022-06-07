# Codigo principal para el MONITOREO constante
# IDENTIFICACION y LOCALIZACION de Tremors No Volcanicos (TNV) en el Valle Medio del Magdalena (VMM)
# Curaduria de Sismicidad - Centro de Transparencia (CDT)
# Autor: Jose Manuel Ramirez Martinez
# Correo: josmramirezmar@unal.edu.co

######################## Configuracion archivo LOG ############################
import sys
import logging
import os 
dirPath = os.getcwd()
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
fh = logging.FileHandler(dirPath + "\\TVN.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(levelname)s %(message)s","%Y/%m/%d %H:%M:%S")
handler.setFormatter(formatter)
fh.setFormatter(formatter)
root.addHandler(handler)
root.addHandler(fh)
with open(dirPath + "\\TVN.log", "a") as file_object:
    file_object.write("\n")
logging.info('***MONITOREO, IDENTIFICACION y LOCALIZACION de Tremors No Volcanicos (TNV)***')
###############################################################################

##################### Declaracion de las librerias  ###########################
try: 
    import time
    t=time.time()
    logging.info("Cargando librerias...")
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import obspy
    import cartopy
    from obspy.clients.fdsn import Client
    from obspy import UTCDateTime,Stream,read_inventory,read
    import obspy.signal
    from os import mkdir
    from threading import Thread
    from datetime import datetime
    import queue
    import TNVfun as tnv
    secs = time.time() - t
    logging.info("Librerias cargadas en " + str(secs) + " segundos.")
except Exception as e:
    logging.error("Error cargando una libreria: " + str(e))
###############################################################################

######################### Funcion principal ###################################
def main():
    # Declaracion de Variables
    #logging.info("Cargando inventario...")
    inv = read_inventory(".\\archivo\\CM.CDT.01.dataless")
    #logging.info("Inventario cargado.")
    #queueR = queue()
    
    # Estaciones del Servicio Geologico Colombiano (SGC)
    #clientCM = Client('http://sismo.sgc.gov.co:8080/')
    #network = "CM"
    #stations = ["CHI","NOR","ROSC","RUS","CVER","VIL","SJC","ZAR","PTB","GUY2C","SPBC","AGCC","VMM09","VMM05","VMM07","VMM10","LL8C","VMM11","VMM12","OCA","BRJC"]
    #channels = "*"
    #locIds = "*"
    #dateStart = UTCDateTime("2022-06-01T00:00:00")
    
    # Carpeta de Almacenamiento
   # arcFolder = "G:\\Mi unidad\\RSUNAL\\TNV\\Python\\TNV\\archive\\"

    # Inicio de hilos
    #downloadDataThread = Thread(target=downloadData, args=(clientCM,network,stations,channels,locIds,dateStart,arcFolder,))
    #downloadDataThread.daemon = True
    #downloadDataThread.start()
    #ReadDataThread = Thread(target=readData, args=(clientCM,network,stations,channelsR,locIds,timeStart,))
    #ReadDataThread.daemon = True
    #ReadDataThread.start()

    #st = read("G:\\Mi unidad\\RSUNAL\\CDT\\Python\\TNV\\CM\\2022\\04\\01\\CM_CHI_2022-04-01.mseed")
    #st.plot(method='full', equal_scale=False)
    #logging.info("Impreso RAW...")
    
    #st.detrend()
    #st.plot(method='full', equal_scale=False)
    #logging.info("Impreso DETREND...")
    
    #st.filter("bandpass", freqmin=1, freqmax=10, corners=2, zerophase=True)
    #st.plot(method='full', equal_scale=False)
    #logging.info("Impreso FILTER...")
    
    #st.normalize(global_max=False) 
    #st.plot(method='full', equal_scale=False)
    #logging.info("Impreso NORMALIZE...")
    
    #st.detrend("linear")
    #logging.info("Impreso DETREND...") 
    
    # Figura mapa de las estaciones
    fig1 = plt.figure("Ortho")
    inv.plot(projection='ortho', method='cartopy', show=False, fig="fig1") # global # local
    fig1.show()
    inv.plot(projection='global', method='cartopy', show=False, fig="fig2") # global # local
    
    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()
###############################################################################