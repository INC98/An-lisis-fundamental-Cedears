import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

resp = requests.get('https://iol.invertironline.com/mercado/cotizaciones/argentina/cedears')
resp = resp.text
soup = BeautifulSoup(resp, 'html.parser')
table = soup.find('table', class_='table')

# creo dos listas vacias para guardar los datos
nombres_cedear = []
montos_operados = []

# recorro la tabla y guardo los datos en las listas vacias
for row in tqdm(table.findAll('tr')[1:]):
    nombre = row.findAll('b')[0].text #texto del b asi solo trae el ticker
    nombres_cedear.append(nombre)
    monto_operado = row.findAll('td')[11].text # texto del monto operado
    montos_operados.append(monto_operado)

# creo el df
df = pd.DataFrame({'Ticker':nombres_cedear,"Montos operados":montos_operados})

# funciones de borrado de \r\n
def clean_ticker(x):
    return x.replace("\r\n","")

def clean_operaciones(x):
    return x.replace("\r\n","")

# aplico los borrados de \r\n
df["Ticker"] = df["Ticker"].apply(lambda x: clean_ticker(x))
df["Montos operados"] = df["Montos operados"].apply(lambda x: clean_operaciones(x))

#borro espacios
df["Ticker"] = df["Ticker"].str.strip() # espacios de principio y final los saco
df["Ticker"] = df["Ticker"].str.replace(r"\s+"," ",regex=True) # espacios multiples que encuentre, pone 1 solo -> los que quedaban sueltos en el medio serian reemplazados por 1 solo espacio
df["Montos operados"] = df["Montos operados"].str.strip() # espacios de principio y final los saco

# borro los puntos de montos operados
df["Montos operados"] = df["Montos operados"].str.replace(".","").astype(float)

#creo un df nuevo usando el anterior para ordenar los valores
df_sorted = df.sort_values("Montos operados",ascending=False)
df_sorted.to_excel('datos2.xlsx', index=False)

lista_valores_liquidez = []
lista_valores_solvencia = []
lista_valores_eficiencia = []
lista_valores_rentabilidad = []
lista_valores_rentabilidad_5a = []
lista_valores_pe_empresa = []
lista_valores_ps_empresa = []
lista_valores_pb_empresa = []
lista_valores_pe_promedio = []
lista_valores_ps_promedio = []
lista_valores_pb_promedio = []
lista_dataframe_ticker = []


#nombres de Tickers ordenados Y HREF PARA BUSCAR EN INVESTING.COM
for item in df_sorted["Ticker"]:
    if item == "DISN":
        item = "DIS"
    elif item == "TEN":
        item = "TS"
    elif item == "BRKB":
        item = "BRKa"
    elif item == "TXR":
        item = "TX"
    elif item == "BA.C":
        item = "BAC"
    elif item == "XROX":
        item = "XRX"
    elif item == "BNG":
        item = "BG"
    elif item == "BBV":
        item = "BBVA"
    elif item == "PKS":
        item = "PKX"
    elif item == "TEFO":
        item = "TEF"
    elif item == "NOKA":
        item = "NOK"
   
    ticker_name = item
    print(ticker_name)
    url_busqueda = ('https://es.investing.com/search/?q=' + ticker_name)
    resp_entities = requests.get(url_busqueda)
    resp_entities = resp_entities.text
    soup_entities = BeautifulSoup(resp_entities, 'html.parser')
    item_buscador = soup_entities.select(".js-inner-all-results-quote-item") # trae los <a>

    for i in item_buscador:
        ticker_name2 = i.select(".second") # de los <a> trae lo que tenga de clase .second osea los spans que tienen el nombre del ticker
        flag = (i.select(".ceFlags")) # de los <a> trae lo que tenga la clase .ceFlags osea los <i> con classname de la bandera
        lista_entities = [flag, ticker_name2]
       
        for j in lista_entities[0]:
            for ñ in lista_entities[1]:
                if j.get("class")[2] == "USA" and ñ.text == ticker_name:
                    href = i.get("href")

                    # ---------- LIQUIDEZ ---------

                    url_ratios = ('https://es.investing.com' + href + '-ratios')
                    
                    # las que la url de la forma mencionada en la linea de arriba no anda, se agregan aca 
                    if url_ratios == "https://es.investing.com/equities/bitfarms-ltd?cid=1173542-ratios":
                        url_ratios = "https://es.investing.com/equities/bitfarms-ltd-ratios"
                    elif url_ratios == "https://es.investing.com/equities/hut-8-mining?cid=1079918-ratios":
                        url_ratios = "https://es.investing.com/equities/hut-8-mining-ratios?cid=1079918"
                    elif url_ratios == "https://es.investing.com/equities/toronto-dominion-bank?cid=20605-ratios":
                        url_ratios = "https://es.investing.com/equities/toronto-dominion-bank-ratios?cid=20605"

                    resp_ratios = requests.get(url_ratios)
                    resp_ratios = resp_ratios.text
                    soup_ratios = BeautifulSoup(resp_ratios, 'html.parser')
                    item_ratios = soup_ratios.select(".noHover")
                    
                    try:
                        liquidez = item_ratios[8].select("td")[5].text
                        if (liquidez != "-"):
                            liquidez=liquidez.replace(".","")
                            liquidez=liquidez.replace(",",".")
                            liquidez = (liquidez.rstrip('%'))
                            liquidez = float(liquidez)
                    except IndexError:
                        continue

                    lista_valores_liquidez.append(liquidez)
                    lista_dataframe_ticker.append(ticker_name)

                    # ---------- SOLVENCIA ---------
                    url_balancesheet = ('https://es.investing.com' + href + '-balance-sheet') # url del balancesheet
                    # las que la url de la forma mencionada en la linea de arriba no anda, se agregan aca
                    if url_balancesheet == "https://es.investing.com/equities/bitfarms-ltd?cid=1173542-balance-sheet":
                        url_balancesheet = "https://es.investing.com/equities/bitfarms-ltd-balance-sheet"
                    elif url_balancesheet == "https://es.investing.com/equities/hut-8-mining?cid=1079918-balance-sheet":
                        url_balancesheet = "https://es.investing.com/equities/hut-8-mining-balance-sheet?cid=1079918"
                    elif url_balancesheet == "https://es.investing.com/equities/toronto-dominion-bank?cid=20605-balance-sheet":
                        url_balancesheet = "https://es.investing.com/equities/toronto-dominion-bank-balance-sheet?cid=20605"

                    resp_balancesheet = requests.get(url_balancesheet)
                    resp_balancesheet = resp_balancesheet.text
                    soup_balancesheet = BeautifulSoup(resp_balancesheet, 'html.parser')
                    item_balancesheet = soup_balancesheet.select(".openTr") # tomo la seccion de la tabla con los valores

                    try:
                        # busco en una lista de tr el span que tenga el nombre de total activos y traigo el primer valor
                        for tr in item_balancesheet:
                            span = tr.find("span")
                            if span and span.text.strip()=="Total activos":
                                total_activos = (tr.select("td")[1].text)  
                    except IndexError:
                        continue

                    total_activos = total_activos.replace(",",".")
                    # a la hora de dividir, si el valor de activo o pasivo corriente es -, dejar resultado en -    

                    try:
                        # busco en una lista de tr el span que tenga el nombre de total pasivo y traigo el primer valor
                        for tr in item_balancesheet:
                            span = tr.find("span")
                            if span and span.text.strip()=="Total pasivo":
                                total_pasivos = (tr.select("td")[1].text)  
                    except IndexError:
                        continue
                    total_pasivos = total_pasivos.replace(",",".")

                   
                    # si hay algun - , el resultado de la division es -
                    if total_activos == "-" or total_pasivos == "-":
                        solvencia = "-"
                    else:
                        solvencia = float(total_activos) / float(total_pasivos)

                    lista_valores_solvencia.append(solvencia)
                    print("lista liquidez: " , len(lista_valores_liquidez))
                    print("lista solvencia: ",len(lista_valores_solvencia))

                    # ---------- EFICIENCIA ----------
                    try:
                        eficiencia = item_ratios[9].select("td")[2].text
                        if (eficiencia != "-"):
                            eficiencia=eficiencia.replace(".","")
                            eficiencia=eficiencia.replace(",",".")
                            eficiencia = (eficiencia.rstrip('%'))
                            eficiencia = float(eficiencia)
                    except IndexError:
                        continue

                    lista_valores_eficiencia.append(eficiencia)
                    print("lista eficiencia: ",len(lista_valores_eficiencia))

                    # ---------- RENTABILIDAD ---------
                    #rentabilidad actual
                    try:
                        rentabilidad = item_ratios[2].select("td")[21].text
                        if (rentabilidad != "-"):
                            rentabilidad=rentabilidad.replace(".","")
                            rentabilidad=rentabilidad.replace(",",".")
                            rentabilidad = (rentabilidad.rstrip('%'))
                            rentabilidad = float(rentabilidad)
                        #print(rentabilidad)
                    except IndexError:
                        continue

                    lista_valores_rentabilidad.append(rentabilidad)
                    print("lista rentabilidad: ",len(lista_valores_rentabilidad))

                    # rentabilidad promedio en 5 años.  Ver si se mantuvo la misma rentabilidad
                    try:
                        rentabilidad_5a = item_ratios[2].select("td")[24].text
                        if (rentabilidad_5a != "-"):
                            rentabilidad_5a=rentabilidad_5a.replace(".","")
                            rentabilidad_5a=rentabilidad_5a.replace(",",".")
                            rentabilidad_5a = (rentabilidad_5a.rstrip('%'))
                            rentabilidad_5a = float(rentabilidad_5a)
                        #print(rentabilidad_5a)
                    except IndexError:
                        continue

                    lista_valores_rentabilidad_5a.append(rentabilidad_5a)
                    print("lista rentabilidad 5a: ",len(lista_valores_rentabilidad_5a))

                    # VALUACION             
                    url_valuacion = ('https://wallmine.com/' + ticker_name)
                    resp_valuacion = requests.get(url_valuacion)
                    resp_valuacion = resp_valuacion.text
                    soup_valuacion = BeautifulSoup(resp_valuacion, 'html.parser')
                    item_valuacion = soup_valuacion.select(".company-peers")
                    count = 0
                    
                    if item_valuacion == []:
                        url_valuacion = 'https://wallmine.com/nasdaq/' + ticker_name
                        resp_valuacion = requests.get(url_valuacion)
                        resp_valuacion = resp_valuacion.text
                        soup_valuacion = BeautifulSoup(resp_valuacion, 'html.parser')
                        item_valuacion = soup_valuacion.select(".company-peers")
                    if item_valuacion == []:
                        url_valuacion = 'https://wallmine.com/nyse/' + ticker_name
                        resp_valuacion = requests.get(url_valuacion)
                        resp_valuacion = resp_valuacion.text
                        soup_valuacion = BeautifulSoup(resp_valuacion, 'html.parser')
                        item_valuacion = soup_valuacion.select(".company-peers")
                    if item_valuacion == []:
                        url_valuacion = 'https://wallmine.com/tsx/' + ticker_name
                        resp_valuacion = requests.get(url_valuacion)
                        resp_valuacion = resp_valuacion.text
                        soup_valuacion = BeautifulSoup(resp_valuacion, 'html.parser')
                        item_valuacion = soup_valuacion.select(".company-peers")
                
                    if url_valuacion == "https://wallmine.com/BRKa":
                        url_valuacion = "https://wallmine.com/nyse/brk-a"

                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    print(url_valuacion)
     
                    try:
                        if item_valuacion == []:    
                            lista_valores_pe_empresa.append("Sin empresa a comparar")
                            lista_valores_ps_empresa.append("Sin empresa a comparar")
                            lista_valores_pb_empresa.append("Sin empresa a comparar")
                            lista_valores_pe_promedio.append("Sin empresa a comparar")
                            lista_valores_ps_promedio.append("Sin empresa a comparar")
                            lista_valores_pb_promedio.append("Sin empresa a comparar")

                            print(lista_valores_pe_empresa)
                            print(lista_valores_pe_promedio)
                            print("valor pe prom",len(lista_valores_pe_promedio))
                            print("valor ps prom",len(lista_valores_ps_promedio))
                            print("valor pb prom",len(lista_valores_pb_promedio))
                        else:
                            # 2 empresas competidoras que aparecen en el grafico
                            pe_empresa1 = item_valuacion[0].select("td")[10].text.strip()
                            ps_empresa1 = item_valuacion[0].select("td")[12].text.strip()
                            pb_empresa1 = item_valuacion[0].select("td")[13].text.strip()
                            pe_empresa1 =pe_empresa1.replace(",","")
                            ps_empresa1 =ps_empresa1.replace(",","")
                            pb_empresa1 =pb_empresa1.replace(",","")

                            pe_empresa2 = item_valuacion[0].select("td")[18].text.strip()
                            ps_empresa2 = item_valuacion[0].select("td")[20].text.strip()
                            pb_empresa2 = item_valuacion[0].select("td")[21].text.strip()
                            
                            count_pe = 3
                            count_ps = 3
                            count_pb = 3
                            pe_empresa = item_valuacion[0].select("td")[2].text.strip()
                            ps_empresa = item_valuacion[0].select("td")[4].text.strip()
                            pb_empresa = item_valuacion[0].select("td")[5].text.strip()
                            pe_empresa =pe_empresa.replace(",","")
                            ps_empresa =ps_empresa.replace(",","")
                            pb_empresa =pb_empresa.replace(",","")
                            lista_valores_pe_empresa.append(pe_empresa)
                            lista_valores_ps_empresa.append(ps_empresa)
                            lista_valores_pb_empresa.append(pb_empresa) 
                            print(lista_valores_pe_empresa)
                            print("valor pe empresa", len(lista_valores_pe_empresa))
                            print("valor ps empresa",len(lista_valores_ps_empresa))
                            print("valor pb empresa",len(lista_valores_pb_empresa))

                            # 2 empresas competidoras que aparecen en el grafico
                            pe_empresa1 = item_valuacion[0].select("td")[10].text.strip()
                            ps_empresa1 = item_valuacion[0].select("td")[12].text.strip()
                            pb_empresa1 = item_valuacion[0].select("td")[13].text.strip()
                            pe_empresa1 =pe_empresa1.replace(",","")
                            ps_empresa1 =ps_empresa1.replace(",","")
                            pb_empresa1 =pb_empresa1.replace(",","")

                            pe_empresa2 = item_valuacion[0].select("td")[18].text.strip()
                            ps_empresa2 = item_valuacion[0].select("td")[20].text.strip()
                            pb_empresa2 = item_valuacion[0].select("td")[21].text.strip()
                            pe_empresa2 =pe_empresa2.replace(",","")
                            ps_empresa2 =ps_empresa2.replace(",","")
                            pb_empresa2 =pb_empresa2.replace(",","")


                            if(pe_empresa == "N/A"):
                                count_pe = count_pe -1
                                pe_empresa = 0.00
                            if(pe_empresa1 == "N/A"):
                                count_pe = count_pe -1
                                pe_empresa1 = 0.00
                            if(pe_empresa2 == "N/A"):
                                count_pe = count_pe -1
                                pe_empresa2 = 0.00

                            if(ps_empresa == "N/A"):
                                count_ps = count_ps -1
                                ps_empresa = 0.00
                            if(ps_empresa1 == "N/A"):
                                count_ps = count_ps -1
                                ps_empresa1 = 0.00
                            if(ps_empresa2 == "N/A"):
                                count_ps = count_ps -1
                                ps_empresa2 = 0.00

                            if(pb_empresa == "N/A"):
                                count_pb = count_pb -1
                                pb_empresa = 0.00
                            if(pb_empresa1 == "N/A"):
                                count_pb = count_pb -1
                                pb_empresa1 = 0.00
                            if(pb_empresa2 == "N/A"):
                                count_pb = count_pb -1
                                pb_empresa2 = 0.00

                            if count_pe != 0:
                                pe_promedio = (float(pe_empresa) + float(pe_empresa1) + float(pe_empresa2)) / count_pe
                                lista_valores_pe_promedio.append(pe_promedio)
                            else:
                                lista_valores_pe_promedio.append("no divisible por cero")
                            print(lista_valores_pe_promedio)
                            print("valor pe prom",len(lista_valores_pe_promedio))
                            
                            if count_ps != 0:
                                ps_promedio = (float(ps_empresa) + float(ps_empresa1) + float(ps_empresa2)) / count_ps
                                lista_valores_ps_promedio.append(ps_promedio)
                            else:
                                lista_valores_ps_promedio.append("no divisible por cero")
                            print("valor ps prom",len(lista_valores_ps_promedio))
                            
                            if count_pb != 0:
                                pb_promedio = (float(pb_empresa) + float(pb_empresa1) + float(pb_empresa2)) / count_pb
                                lista_valores_pb_promedio.append(pb_promedio)
                            else:
                                lista_valores_pb_promedio.append("no divisible por cero")
                            print("valor pb prom",len(lista_valores_pb_promedio))
                            
                    except IndexError: # si no tiene tablita o tiene menos de 3 competidores
                            count_pe = 2
                            count_ps = 2
                            count_pb = 2
                            pe_empresa = item_valuacion[0].select("td")[2].text.strip()
                            ps_empresa = item_valuacion[0].select("td")[4].text.strip()
                            pb_empresa = item_valuacion[0].select("td")[5].text.strip()
                            pe_empresa =pe_empresa.replace(",","")
                            ps_empresa =ps_empresa.replace(",","")
                            pb_empresa =pb_empresa.replace(",","")
                            lista_valores_pe_empresa.append(pe_empresa)
                            lista_valores_ps_empresa.append(ps_empresa)
                            lista_valores_pb_empresa.append(pb_empresa) 
                            print(lista_valores_pe_empresa)
                            print("valor pe empresa", len(lista_valores_pe_empresa))
                            print("valor ps empresa",len(lista_valores_ps_empresa))
                            print("valor pb empresa",len(lista_valores_pb_empresa))

                            # 2 empresas competidoras que aparecen en el grafico
                            pe_empresa1 = item_valuacion[0].select("td")[10].text.strip()
                            ps_empresa1 = item_valuacion[0].select("td")[12].text.strip()
                            pb_empresa1 = item_valuacion[0].select("td")[13].text.strip()
                            pe_empresa1 =pe_empresa1.replace(",","")
                            ps_empresa1 =ps_empresa1.replace(",","")
                            pb_empresa1 =pb_empresa1.replace(",","")

                            if(pe_empresa == "N/A"):
                                count_pe = count_pe -1
                                pe_empresa = 0.00
                            if(pe_empresa1 == "N/A"):
                                count_pe = count_pe -1
                                pe_empresa1 = 0.00

                            if(ps_empresa == "N/A"):
                                count_ps = count_ps -1
                                ps_empresa = 0.00
                            if(ps_empresa1 == "N/A"):
                                count_ps = count_ps -1
                                ps_empresa1 = 0.00

                            if(pb_empresa == "N/A"):
                                count_pb = count_pb -1
                                pb_empresa = 0.00
                            if(pb_empresa1 == "N/A"):
                                count_pb = count_pb -1
                                pb_empresa1 = 0.00

                        
                            if count_pe != 0:
                                pe_promedio = (float(pe_empresa) + float(pe_empresa1)) / count_pe
                                lista_valores_pe_promedio.append(pe_promedio)
                            else:
                                lista_valores_pe_promedio.append("no divisible por cero")
                            print(lista_valores_pe_promedio)
                            print("valor pe prom",len(lista_valores_pe_promedio))
                            
                            if count_ps != 0:
                                ps_promedio = (float(ps_empresa) + float(ps_empresa1))  / count_ps
                                lista_valores_ps_promedio.append(ps_promedio)
                            else:
                                lista_valores_ps_promedio.append("no divisible por cero")
                            print("valor ps prom",len(lista_valores_ps_promedio))
                            
                            if count_pb != 0:
                                pb_promedio = (float(pb_empresa) + float(pb_empresa1) ) / count_pb
                                lista_valores_pb_promedio.append(pb_promedio)
                            else:
                                lista_valores_pb_promedio.append("no divisible por cero")
                            print("valor pb prom",len(lista_valores_pb_promedio))
                            continue
                             
df_resultado = pd.DataFrame(({"Ticker":lista_dataframe_ticker,"Liquidez":lista_valores_liquidez,"Solvencia":lista_valores_solvencia,"Eficiencia":lista_valores_eficiencia,"Rentabilidad":lista_valores_rentabilidad, "Rentabilidad promedio 5A":lista_valores_rentabilidad_5a,"P/E empresa":lista_valores_pe_empresa,"P/E industria":lista_valores_pe_promedio,"P/S empresa":lista_valores_ps_empresa,"P/S industria":lista_valores_ps_promedio,"P/B empresa":lista_valores_pb_empresa,"P/B industria":lista_valores_pb_promedio}))
df_resultado.to_excel('reporte_cedears.xlsx', index=False)
