# # Codigo secuencial para tratamiento de formas de onda
# ## IDENTIFICACION y LOCALIZACION de Tremors No Volcanicos (TNV) en el Valle Medio del Magdalena (VMM)
# ## Curaduria de Sismicidad - Centro de Transparencia (CDT)
# ### Autor: Jose Manuel Ramirez Martinez
# ### Correo: josmramirezmar@unal.edu.co

######################## Configuracion archivo LOG ############################
import sys
import logging
import os 
dirPath = os.getcwd()
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
fh = logging.FileHandler(dirPath + "\\TVNsec.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(levelname)s %(message)s","%Y/%m/%d %H:%M:%S")
handler.setFormatter(formatter)
fh.setFormatter(formatter)
root.addHandler(handler)
root.addHandler(fh)
with open(dirPath + "\\TVNsec.log", "a") as file_object:
    file_object.write("\n")
logging.info('***MONITOREO, IDENTIFICACION y LOCALIZACION de Tremors No Volcanicos (TNV)***')
###############################################################################

# Declaracion de las librerias
try: 
    import time
    t=time.time()
    logging.info("Cargando librerias...")
    import os
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import cartopy
    from threading import Thread
    import obspy
    from obspy.clients.fdsn import Client as ClientF 
    from obspy import UTCDateTime,Stream,read_inventory
    from obspy.signal.trigger import z_detect,plot_trigger
    from xcorr import correlate_maxlag, correlate_template, get_lags
    secs = time.time() - t
    logging.info("Librerias cargadas en " + str(secs) + " segundos.")
except Exception as e:
    logging.error("Error cargando una libreria: " + str(e))

# Lectura del Inventario
inv = read_inventory(".\\archivo\\dataless\\CM.CDT.04.dataless")
inv = inv.select(channel="[HH]*")
logging.info(inv)

# Parametros Estaciones del Servicio Geologico Colombiano (SGC)
clientCM = ClientF('http://sismo.sgc.gov.co:8080/')
network = "CM"
#stations = ("CHI","NOR","ROSC","RUS","CVER","VIL","SJC","ZAR","PTB","GUY2C","SPBC","AGCC","EZNC","VMM09","VMM05","VMM07","VMM10","LL8C","VMM11","VMM12","OCA","BRJC")
stations = ("ZAR","PTB","AGCC","EZNC","VMM09","VMM05","VMM07","VMM10","VMM11","VMM12","OCA")
channels = ("HHN","HHE","HHZ")
locIds = "*"
dateStart = UTCDateTime("2022-06-01T00:00:00")

# Bucle multiple
while(dateStart < UTCDateTime.now()):
    DateEnd = dateStart + (4*60)

    # Directorio de resultados
    dirResultado = "archivo\\" + network + "\\" + dateStart.strftime("%Y") + "\\" + dateStart.strftime("%m") + "\\" + dateStart.strftime("%d") + "\\" + dateStart.strftime("%H%M")
    mseedName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M")
    dirMseed = os.path.join(dirPath, dirResultado, mseedName)
    dirFull = os.path.dirname(dirMseed)

    if not os.path.exists(dirFull):
        os.makedirs(dirFull)
        logging.info("Creado el directorio " + dirFull)
    else: 
        logging.warning("Directorio " + dirFull + " existente.")

    # Carga de Stream
    st = Stream()
    for sta in stations:
        for cha in channels:
            try:
                st += clientCM.get_waveforms('CM', sta, '*', cha, dateStart, DateEnd)
                logging.info("Obteniendo el " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " del canal " + str(cha) + " de la estacion " + str(sta) + "." )
            except Exception as e:
                logging.error("Error obteniendo el " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " del canal " + str(cha) + " de la estacion " + str(sta) + ": " + str(e))

    # Impresion en consola
    logging.info(st)

    # Almacenado temporal
    try:
        st.write(dirMseed, format="MSEED")
        logging.info("mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " almacenado correctamente.")
    except Exception as e:
        logging.error("Error almacenando el mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))

    # Plot RAW
    rawName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_RAW.png"
    dirRaw = os.path.join(dirPath, dirResultado, rawName)

    # Seleccion de componente
    #st = st.select(component="Z")

    try:
        st.plot(method='full', equal_scale=False, outfile=dirRaw)
        logging.info("RAW mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
    except Exception as e:
        logging.error("Error ploteando el RAW mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))

    # Plot DETREND
    detName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_DET.png"
    dirDet = os.path.join(dirPath, dirResultado, detName)

    try:
        st.detrend()
        st.plot(method='full', equal_scale=False, outfile=dirDet)
        logging.info("DETREND mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
    except Exception as e:
        logging.error("Error ploteando el DETREND del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))

    # Plot FILTRO
    filName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_FIL.png"
    dirFil = os.path.join(dirPath, dirResultado, filName)

    try:
        st.filter("bandpass", freqmin=1, freqmax=10, corners=2, zerophase=True)
        st.plot(method='full', equal_scale=False, outfile=dirFil)
        logging.info("FILTRAO mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
    except Exception as e:
        logging.error("Error ploteando el FILTRADO del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))
        
    # Plot RESPUESTA INSTRUMENTAL
    RIName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_RI.png"
    dirRI = os.path.join(dirPath, dirResultado, RIName)

    try:
        st.remove_response(inventory=inv, output="DEF", water_level=60, fig=dirRI)
        logging.info("RESPUESTA INSTRUMENTAL mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
    except Exception as e:
        logging.error("Error ploteando LA RESPUESTA INSTRUMENTAL del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))
        
    # Plot MERGE
    MerName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_MER.png"
    dirMer = os.path.join(dirPath, dirResultado, MerName)


    try:
        st.merge(method=1, fill_value='interpolate', interpolation_samples=-1)
        st.plot(method='full', equal_scale=False, outfile=dirMer)
        logging.info("Trazas del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " unidas correctamente.")
    except Exception as e:
        logging.error("Error unindo las trazas del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))

    # Plot NORMALIZADO
    norName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_NOR.png"
    dirNor = os.path.join(dirPath, dirResultado, norName)

    try:
        st.normalize(global_max=False) 
        st.plot(method='full', equal_scale=False, outfile=dirNor)
        logging.info("NORMALIZADO mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
    except Exception as e:
        logging.error("Error ploteando el NORMALIZADO del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))
        
    # Plot COMPONENTE Z
    zName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_Z.png"
    dirZ = os.path.join(dirPath, dirResultado, zName)

    try:
        st2 = st.select(component="Z")
        st2.plot(method='full', equal_scale=False, outfile=dirZ)
        logging.infont("COMPONENTE Z mseed del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
    except Exception as e:
        logging.error("Error ploteando el COMPONENTE Z del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))
    
    # CORRELACION CRUZADA (xcorr)
    maxlag = 10

    for tr1 in st2:
        a = tr1.data
        aName = tr1.id
        
        for tr2 in st2:
            b = tr2.data
            bName = tr2.id
            
            corrName = network + "_" + dateStart.strftime("%Y-%m-%dT%H-%M") + "_CORR_" + aName[3:-7] + "-" + bName[3:-7] + ".png"
            dirCORR = os.path.join(dirPath, dirResultado, corrName)
            
            try:
                cc1 = correlate_maxlag(a, b, maxlag)

                grid = plt.GridSpec(2, 1, wspace=0.4, hspace=0.3)
                ax1 = plt.subplot(grid[0, 0])
                ax2 = plt.subplot(grid[1, 0])
                ax1.plot(np.arange(len(a)), a, label='signal {}'.format(aName))
                ax1.plot(np.arange(len(b)), b, label='signal {}'.format(bName))
                ax2.plot(get_lags(cc1), cc1)
                ax1.legend(loc=3)
                kw = dict(xy=(0.05, 0.95), xycoords='axes fraction', va='top')
                ax2.annotate('correlate_maxlag(a, b, {})'.format(maxlag), **kw)
                plt.savefig(dirCORR)
                
                logging.info("_CORR_" + aName[3:-7] + "-" + bName[3:-7] + " del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + " ploteado correctamente.")
            except Exception as e:
                logging.error("Error ploteando _CORR_" + aName[3:-7] + "-" + bName[3:-7] + " del " + str(dateStart.strftime("%Y-%m-%dT%H:%M")) + ": " + str(e))
        
    dateStart = dateStart + (2*60)


