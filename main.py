'''

Project 1

Challenge:

Get data from the results at UNAM
Tip: use beautifulsoup module, to install it from jupyter notebook try: 

pip install beautifulsoup4

make a research to learn how to get the data for your bachelor degree and compare histograms of scores with another bachelors like the Arts or law career applicants.
get an statistical analysis :)You can check some on these links:

MODALIDAD ESCOLARIZADA
Área 1: https://www.dgae.unam.mx/Junio2018/resultados/15.html
Área 2: https://www.dgae.unam.mx/Junio2018/resultados/25.html
Área 3: https://www.dgae.unam.mx/Junio2018/resultados/35.html
Área 4: https://www.dgae.unam.mx/Febrero2018/resultados/45.html

'''

import pandas as pd
import numpy as np
import requests

from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

na = lambda t: np.nan if t.strip() is "" else t

def fac_results(u):
    page = requests.get(u)
    soup = BeautifulSoup(page.content, 'html.parser')
    results_table = soup.find("table", class_="results")
    
    table_head = results_table.find("thead")
    table_body = results_table.find("tbody")

    headers = [th.text for th in table_head.findAll("th")][:3]
    results = [[na(td.text) for td in tr.findAll("td")][:3] for tr in table_body.findAll("tr")]

    df = pd.DataFrame(results, columns=headers)
    return df

def find_carreer(el):
    parent_div = el.find_parent("div")
    h3 = parent_div.find("h3")
    return h3.text.strip()

def get_area_results(url):
    facspage = requests.get(url)
    facssoup = BeautifulSoup(facspage.content, 'html.parser')

    all_results = [{"fac": a.text.strip(), "car": find_carreer(a), "res": fac_results(resultados_url+a["href"])} for a in facssoup.findAll("a", class_=["btn", "btn-link"])]

    for res in all_results:
        res["res"]["Carrera"] = res["car"]
        res["res"]["Facultad"] = res["fac"]

    final_results = pd.concat([r["res"] for r in all_results])
    return final_results

def analyze_results(res, nam):
    presented_results = res.copy()
    presented_results = presented_results.dropna(subset=['Aciertos'])
    presented_results["Aciertos"] = presented_results["Aciertos"].astype(int)
    presented_results_hist = presented_results.copy()
    presented_results = presented_results.dropna(subset=['Seleccionado'])
    presented_results["Seleccionado"] = presented_results["Aciertos"].astype(str)
    # presented_results.head()
    
    carreras = presented_results.groupby("Carrera")
    counts = [[car, presented_results.loc[carreras.groups[car]]["Aciertos"].count()] for car in carreras.groups.keys()]
    carreras_count = pd.DataFrame(counts, columns=['Carrera', 'Count'])
    
    facultades = presented_results.groupby("Facultad")
    counts = [[car, presented_results.loc[facultades.groups[car]]["Aciertos"].count()] for car in facultades.groups.keys()]
    facultades_count = pd.DataFrame(counts, columns=['Facultad', 'Count'])

    return {
        "area": nam,
        "all_res": presented_results_hist,
        "car_cnt": carreras_count,
        "fac_cnt": facultades_count
    }



if __name__ == "__main__":
    resultados_url = "https://www.dgae.unam.mx/Junio2018/resultados/"

    areas = {
        "Area1": "https://www.dgae.unam.mx/Junio2018/resultados/15.html",
        "Area2": "https://www.dgae.unam.mx/Junio2018/resultados/25.html",
        "Area3": "https://www.dgae.unam.mx/Junio2018/resultados/35.html",
        "Area4": "https://www.dgae.unam.mx/Junio2018/resultados/45.html"
    }

    resultados = [get_area_results(areas[area]) for area in areas.keys()]



    

    results = [analyze_results(resu, area) for idx, (resu, area) in enumerate(zip(resultados, areas.keys()))]

    for idx, res in enumerate(results):
        plt.figure(idx)
        
        plt.subplot(212)
        plt.xticks(rotation=90)
        plt.title(res["area"])
        plt.hist(res["all_res"]["Aciertos"], bins=20)

        plt.subplot(221)
        plt.xticks(rotation=90)
        plt.title(res["area"])
        plt.barh(res["car_cnt"]["Carrera"], res["car_cnt"]["Count"])
        # plt.barh(res["car_cnt"]["Carrera"], res["all_res"][""])
        # new_df = pd.DataFrame()

        # # new_df = pd.concat([res["car_cnt"]["Carrera"], res["car_cnt"]["Count"]], axis=1)

        # new_df.plot.bar(new_df)

        plt.subplot(222)
        plt.xticks(rotation=90)
        plt.title(res["area"])
        plt.barh(res["fac_cnt"]["Facultad"], res["fac_cnt"]["Count"])

        plt.show()

    for idx, (basefinal, area) in enumerate(zip(resultados, areas.keys())):
        print("\n+++++ {} +++++".format(area))
        basefinal["Aciertos"] = basefinal["Aciertos"].astype(float)
        agrupado5 = basefinal[basefinal['Aciertos'].notnull()].groupby('Carrera').mean()
        print(agrupado5[agrupado5['Aciertos']==agrupado5['Aciertos'].min()])
    
    for idx, (basefinal, area) in enumerate(zip(resultados, areas.keys())):
        print("\n+++++ {} +++++".format(area))
        basefinal["Aciertos"] = basefinal["Aciertos"].astype(float)
        agrupado5 = basefinal[basefinal['Aciertos'].notnull()].groupby('Carrera').mean()
        print(agrupado5[agrupado5['Aciertos']==agrupado5['Aciertos'].max()])

    for idx, (basefinal, area) in enumerate(zip(resultados, areas.keys())):
        print("\n+++++ {} +++++".format(area))
        basefinal["Aciertos"] = basefinal["Aciertos"].astype(float)
        agrupado5 = basefinal[basefinal['Aciertos'].notnull()].groupby('Carrera').describe()
        print(agrupado5)

