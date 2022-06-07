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
fh = logging.FileHandler(dirPath + "\\TVNfdsn.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(levelname)s %(message)s","%Y/%m/%d %H:%M:%S")
handler.setFormatter(formatter)
fh.setFormatter(formatter)
root.addHandler(handler)
root.addHandler(fh)
with open(dirPath + "\\TVNfdsn.log", "a") as file_object:
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
    
    
    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()
###############################################################################