import tkinter as tk
from tkinter import ttk
import ollama
import json

# Initialiser le client Ollama
client = ollama.Client()
model = "deepseek-llm"

# Ouverture du fichier de Cv
with open('Cv.json', 'r', encoding='utf-8') as file:
    cv_data = json.load(file)

# L'avant prompt qui est la partie la plus importante !!!
context = f"""
Tu disposes d'informations personnelles sur une personne nommée Amazigh :
A propos de lui : {cv_data['A propos de moi']}
Son éducation : {cv_data['education']}
Ses expériences : {cv_data['experiences']}
Ses projets : {cv_data['projects']}
Les langues qu'il maitrise : {cv_data['languages']}
Ses activités préférées : {cv_data['activities']}

Quand on te pose une question, tu dois répondre **comme si tu étais Amazigh** en suivant **strictement** les règles suivantes :

- Tu réponds à la première personne, comme si tu parlais de toi-même.
- Ta réponse doit être **ultra concise** : pas de détails inutiles, pas de justifications.
- **Tu ne dois jamais mentionner, citer ou faire référence aux données ci-dessus.**
- Si la réponse n'est pas explicitement présente, **déduis-la intelligemment**, sans le dire, et **sans expliquer** ton raisonnement.
- Si l'information est totalement absente, tu réponds simplement **"Je préfère ne pas répondre."**
- Tu ne dois jamais dire "comme indiqué ci-dessus", "comme mentionné", "d'après les projets", etc.

Maintenant, si c'est une questions  réponds comme si tu étais Amazigh si ce n'est pas une question réponds normalement et naturellement :"""


# La classe de l'interface graphique 
class ChatBotGUI:

    def __init__(self, root):
        # L'initialisation de l'origine root
        self.root = root
        self.root.title("💬 ChatBot Amazigh")
        self.root.configure(bg="#f0f2f5")

        # Le chat Frame
        self.chat_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        # Canvas pour les messages scrollé
        self.canvas = tk.Canvas(self.chat_frame, bg="#f0f2f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f2f5")

        # pour ajuster la taille de scrollable_frame automatiquement !
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # création de la fenêtre canva et remplissage automatique de l'espace
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window, width=e.width
            )
        )

        # configuration du scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Le frame de l'entree utilisateur
        self.entry_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)
        self.entry = tk.Entry(self.entry_frame, font=("Segoe UI", 11), bg="#ffffff", fg="#333333", relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        # Button d'envoie du message
        self.send_button = tk.Button(
            self.entry_frame, text="Send", font=("Segoe UI", 10, "bold"),
            bg="#0078D7", fg="white", activebackground="#005a9e",
            relief=tk.FLAT, padx=20, pady=6, command=self.send_message, cursor="hand2"
        )
        self.send_button.pack(side=tk.RIGHT)

    # fonction d'envoie du message à deepseek
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.add_message("Vous", user_input, "user")
            bot_response = self.get_bot_response(user_input,context)
            self.add_message("Amazigh", bot_response, "bot")
            self.entry.delete(0, tk.END)

    # Rajout du message du bot/user dans l'interface
    def add_message(self, sender, message, side):
        container = tk.Frame(self.scrollable_frame, bg="#f0f2f5")
        container.pack(anchor="e" if side == "user" else "w", pady=4, fill=tk.X, padx=6)

        # Le nom du label bot/user
        name = tk.Label(container, text=sender, font=("Segoe UI", 8, "bold"), bg="#f0f2f5", fg="#555")
        name.pack(anchor="e" if side == "user" else "w", padx=10)

        # Bubble styling (couleurs/position)
        bubble_color = "#DCF8C6" if side == "user" else "#FFFFFF"
        anchor = "e" if side == "user" else "w"
        justify = "right" if side == "user" else "left"

        bubble = tk.Label(
            container,
            text=message,
            wraplength=280,
            justify=justify,
            font=("Segoe UI", 10),
            bg=bubble_color,
            fg="#000000",
            padx=12,
            pady=8,
            bd=0,
            relief=tk.FLAT
        )
        bubble.config(borderwidth=5, highlightthickness=0)
        bubble.pack(anchor=anchor,padx=10)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def get_bot_response(self, question,context):
        prompt = context + question  
        response = client.generate(model=model, prompt=prompt)
        return response['response']

        

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatBotGUI(root) # lancer l'interface graphique
    bonjour = gui.get_bot_response("Bonjour monsieur!","") # Pour que le chatbot nous salue !
    gui.add_message("Amazigh", bonjour, "bot") # rajouter le salue !
    root.mainloop() # boucle de la GUI
