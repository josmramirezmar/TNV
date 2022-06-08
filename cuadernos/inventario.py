# Codigo revision Inventario (Dataless)
# IDENTIFICACION y LOCALIZACION de Tremors No Volcanicos (TNV) en el Valle Medio del Magdalena (VMM)
# Curaduria de Sismicidad - Centro de Transparencia (CDT)
# Autor: Jose Manuel Ramirez Martinez
# Correo: josmramirezmar@unal.edu.co

##################### Declaracion de las librerias  ###########################
try: 
    import time
    t=time.time()
    print("Cargando librerias...")
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import cartopy
    from obspy import read_inventory
    secs = time.time() - t
    print("Librerias cargadas en " + str(secs) + " segundos.")
except Exception as e:
    print("Error cargando una libreria: " + str(e))
###############################################################################

######################## Lectura del Inventario  ##############################
try: 
    inv = read_inventory("..\\archivo\\dataless\\CM.CDT.04.dataless")
    inv = inv.select(channel="[HH]*")
    print(inv)
    inv.plot(projection='ortho', method='cartopy') # global # local
except Exception as e:
    print("Error leyendo el inventario: " + str(e))
###############################################################################