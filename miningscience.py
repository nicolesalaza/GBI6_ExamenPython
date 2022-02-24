from Bio import Entrez 
from Bio import SeqIO 
from Bio import GenBank 
import re

def download_pubmed(keyword):
    """La función download_pubmed son palabras claves para realizar una busqueda en Pubmed. 
    keyword: son palabras claves de búsqueda"""

    Entrez.email = "nikisalazar15@gmail.com"
    Entr=Entrez.read(Entrez.esearch(db="pubmed",
                        term= keyword,
                        usehistory="y"))
    
    webenv=Entr["WebEnv"]
    query_key=Entr["QueryKey"]
    handle=Entrez.efetch(db="pubmed",
                      rettype='medline',
                      retmode="text",
                      retstart=0,
                      retmax=543, webenv=webenv, query_key=query_key)
    out_handle = open(keyword+".txt", "w")
    data=handle.read()
    out_handle.write(data)
    out_handle.close()
    handle.close()
    return data

def mining_pubs(tipo, archivo):
    """La función mining_pubs recibe dos argumentos, que corresponde al tipo de minado de datos que se desea y el documento del 
    cual se va a extraer los datos.
           "DP" --> recupera el año de publicación del artículo. El retorno es un dataframe con el PMID y el DP_year.
           "AU" --> recupera el número de autores por PMID. El retorno es un dataframe con el PMID y el num_auth.
           "AD" -->recupera el conteo de autores por país. El retorno es un dataframe con el country y el num_auth."""
    
    import csv
    import re
    import pandas as pd
    from collections import Counter
    with open(archivo+".txt", errors="ignore") as f: 
        texto = f.read() 
    if tipo == "DP":
        PMID = re.findall("PMID-\s\d{8}", texto)
        PMID = "".join(PMID)
        PMID = PMID.split("PMID- ")
        year = re.findall("DP\s{2}-\s(\d{4})", texto)
        pmid_y = pd.DataFrame()
        pmid_y["PMID"] = PMID
        pmid_y["Año de publicación"] = year
        return (pmid_y)
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", texto) 
        autores = texto.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        pmid_a = pd.DataFrame()
        pmid_a["PMID"] = PMID 
        pmid_a["Numero de autores"] = num_autores
        return (pmid_a)
    elif tipo == "AD": 
        texto = re.sub(r" [A-Z]{1}\.","", texto)
        texto = re.sub(r"Av\.","", texto)
        texto = re.sub(r"Vic\.","", texto)
        texto = re.sub(r"Tas\.","", texto)
        AD = texto.split("AD  - ")
        n_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        n_paises.append(pais[0])
        conteo=Counter(n_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        veces_pais = pd.DataFrame()
        veces_pais["pais"] = resultado.keys()
        veces_pais["numero de autores"] = resultado.values()
        return (veces_pais)