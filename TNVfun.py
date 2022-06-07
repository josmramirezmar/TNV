# Codigo funciones para el MONITOREO constante
# IDENTIFICACION y LOCALIZACION de Tremors No Volcanicos (TNV) en el Valle Medio del Magdalena (VMM)
# Curaduria de Sismicidad - Centro de Transparencia (CDT)
# Autor: Jose Manuel Ramirez Martinez
# Correo: josmramirezmar@unal.edu.co

################ Declaracion de la funcion para archivo #######################
def makeFileSGC(st,startDateD,net,sta,folderD):
    file = net + "\\" + str(startDateD.strftime("%Y")) + "\\" + str(startDateD.strftime("%m")) + "\\" + str(startDateD.strftime("%d")) + "\\" + net + "_" + sta + "_" + str(startDateD.strftime("%Y-%m-%dT%H-%M")) + ".mseed"
    outputFile = folderD + file
    directory = os.path.dirname(outputFile)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if not os.path.isfile(outputFile):
        try:
            st.write(outputFile, format="MSEED") # esta fallando 
            logging.info("Guardando el " + str(startDateD.strftime("%Y-%m-%dT%H:%M")) + " de la estacion " + str(sta))
        except Exception as e:
            logging.warning("Error guardando el " + str(startDateD.strftime("%Y-%m-%dT%H:%M")) + " de la estacion " + str(sta) + ": " + str(e)) 
    else:
        logging.info("MSEED del " + str(startDateD.strftime("%Y-%m-%dT%H:%M")) + " de la estacion " + str(sta) + " previamente guardado")
###############################################################################

################ Declaracion del hilo de descarga del SGC #####################
def downloadData(cli,net,stationsD,channels,ids,startDateD,folderD):
    logging.info("->Empezando hilo de descarga del SGC")
    endDateD = UTCDateTime.now()
    logging.info("Descargando desde " + str(startDateD) + " hasta " + str(endDateD) + " ...")
    
    while startDateD < endDateD:
        date = str(startDateD.strftime("%Y-%m-%dT%H:%M"))
        lastDateD = startDateD + (4 * 60)
        
        logging.info("Descargando el " + date + " ...")
        for sta in stationsD:
            st = Stream()
            
            try:
                logging.info("Descargado el " + date + " de la estacion " + str(sta) + "...")
                st = cli.get_waveforms(net,sta,channels,ids,startDateD,lastDateD)
                print(st)
                makeFileSGC(st,startDateD,net,sta,folderD)
            except Exception as e:                               
                logging.warning("Error con la descarga del " + date + " de la estacion " + str(sta) + ": " + str(e))
                continue
        logging.info("Descarga del " + date + " finalizada.")
        
        # Incremento de 2 min
        startDateD = startDateD + (2 * 60)
    logging.info("Descarga finalizada.")
###############################################################################