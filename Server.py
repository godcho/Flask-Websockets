#!/usr/bin/env python
# -*- coding: utf-8 -*-
# dans le répertoire mon_projetRest lancer : python app/restPostGet.py
# Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

from math import *
import json
from flask import Flask, jsonify, request,abort,render_template
from flask_socketio import SocketIO, emit

#Démarrage Flask et WebSockets
app = Flask(__name__)
socketio = SocketIO(app)
###############################
calculs = [
    {
        'id_Calcul':122,
        'Largeur': 1,
        'Ent_Axe': 2,
        'aY': 4,
        'Resultat_Debit_Theorique':145,
        'Resultat_Puissance_Utile':145,
        'Resultat_Tension_Service':145,
        'done': False
    },
    {
        'id_Calcul': 123,
        'Largeur': 20,
        'Ent_Axe': 2,
        'aY': 4,
        'Resultat_Debit_Theorique':245,
        'Resultat_Puissance_Utile':245,
        'Resultat_Tension_Service':245,
        'done': False
    },
]


@app.route('/')
def index():
    return render_template('index.html')
    

def create_calcul(largeur,ent_axe,angle):
    
    calcul = {
        'id_Calcul': calculs[-1]['id_Calcul'] + 1,
        'Largeur': largeur,
        'Ent_Axe': ent_axe,
        'aY':angle,
        'done': False
    }
    # enregistrement des résultats dans 'calculs' puis retour des valeurs par le service
    calcul["Resultat_Debit_Theorique"]=largeur*ent_axe
    calcul["Resultat_Puissance_Utile"]=largeur*angle
    calcul["Resultat_Tension_Service"]=ent_axe*angle
    calculs.append(calcul)
    return calcul
    
#########################################################################
### Les Sockets...###
#########################################################################
@socketio.on('connexion')
def on_connect(message):
    print message['data']
    
@socketio.on('value changed')
def value_changed(message):
    ##print message['who']+" : "+message['data']
    print type(message)
    print message
    ## Si envoie automatique des valeurs du formulaire.
    ## Le traitement au niveau serveur est + lourd car il faut 
    ## récupérer des json dans un tableau : message[0]["value"] par exemple
    #print message[0]['value']
    # Si le Json est forger au départ sous la forme -> {Largeur:12,EntAxe:14,Angle:45}
    # on peut traiter plus clairement...
    print message["Largeur"]
    print message["EntAxe"]
    print message["Angle"]
    ########## Valeurs récupérées de la form pour le calcul
    results = create_calcul(message["Largeur"],message["EntAxe"],message["Angle"])
    print ("Résultats : ")
    print results["Resultat_Debit_Theorique"]
    print results["Resultat_Puissance_Utile"]
    print results["Resultat_Tension_Service"]
    print ("-------------------------------")
    for calcul in calculs:
        ##print calcul.get("id_Calcul")
        print calcul['id_Calcul']
    print("--------------------------------")
    #emit('update value', message, broadcast=True)
    emit('update value',results, broadcast=True)
    ########## Génération d'un calcul de test...
    results = create_calcul(10,10,25)
    print ("Résultats : ")
    print results["Resultat_Debit_Theorique"]
    print results["Resultat_Puissance_Utile"]
    print results["Resultat_Tension_Service"]
    print ("-------------------------------")
    for calcul in calculs:
        print calcul['id_Calcul']
    print("--------------------------------")
    #emit('update value', message, broadcast=True)
    #emit('update value',results, broadcast=True)
    
#########################################################################
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=True)