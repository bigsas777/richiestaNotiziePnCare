from flask import Flask, Response, jsonify
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

@app.route('/')
def richiestaNotizie():
    url = "https://www.comune.pordenone.it/it"                 #  pncare.pythonanywhere.com

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    listaNotizie = doc.find_all("ul")[6]

    notizie_pronte = []

    for i in range(6):
        obj_notizia = {"Indice": "", "Link": "", "Titolo": "", "Descrizione": "", "Data": "", "Immagine": ""}

        notizia = listaNotizie.find_all("li")[i]

        # INDICE NOTIZIA
        obj_notizia["Indice"] = i

        # LINK NOTIZIA
        link = notizia.h3
        link = link.a.attrs['href']
        obj_notizia["Link"] = link

        # TITOLO NOTIZIA
        titolo = notizia.h3.string
        obj_notizia["Titolo"] = titolo

        # DESCRIZIONE NOTIZIA
        descrizione = notizia.find(class_="collectionItemDescription")
        descrizione = descrizione.find(class_="description")
        descrizione = descrizione.span.string
        obj_notizia["Descrizione"] = descrizione

        # DATA NOTIZIA
        data = notizia.find(class_="collectionItemDates")

        giorno = data.find(class_="collectionItemDateDay")
        giorno = giorno.string.strip()

        mese = data.find(class_="collectionItemDateMonth")
        mese = mese.string.strip()

        anno = data.find(class_="collectionItemDateYear")
        anno = anno.string.strip()

        data = giorno + " " + mese + " " + anno
        data = str(data)

        obj_notizia["Data"] = data

        # IMMAGINE NOTIZIA
        img = notizia.img.attrs['src']
        obj_notizia["Immagine"] = img

        notizie_pronte.append(obj_notizia)

    return jsonify(notizie_pronte)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
