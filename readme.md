Ce document décrit le projet du module Linguistique L3 année 2025

Fait par : ADJLOUT Amazigh

D'abord il faut installer ollama localement :  
    curl -fsSL https://ollama.com/install.sh | sh

il faut aussi que Python3 soit installé:
    sudo apt install python3

et il faut installer le module ollama et tkinter pour python:
    pip install ollama
    sudo apt-get install python3-tk

ensuite il faut créer un evironemment python (chatbot) et l'activer:
    python3 -m venv chatbot
    source chatbot/bin/activate

et pour finir j'ai choisi comme llm deepseek
    ollama pull deepseek-llm

pour lancer le programme et l'interface graphique:
    python3 chatbot.py

Des question pour vos tests sont disponible dans "questions.txt" !


