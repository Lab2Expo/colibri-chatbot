import os
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Lista FAQ: parole chiave + risposta + tipo matching ("all" o "any")
responses = [
    (["dove", "bottega"], "Puoi trovare la nostra Bottega in centro a Monselice in Via Roma 26, Monselice (PD) — 35043. https://equocolibri.org", "all"),
    (["orari", "apertura"], "Solitamente i giorni di apertura sono: lunedì, mercoledì, giovedì, venerdì e sabato 9:30–12:00 e 15:30–19:00; Puoi anche contattarci direttamente su Instagram! https://www.instagram.com/ilcolibri.monselice/", "all"),
    (["contattare", "informazioni"], "Se vuoi informazioni di qualunque genere scrivici su Instagram! https://www.instagram.com/ilcolibri.monselice/", "any"),
    (["negozio", "online", "spedizione"], "Noi non abbiamo un negozio online perché per noi è importante comunicare direttamente al cliente. In Bottega potrai fare un viaggio nel mondo del commercio Equo.", "all"),
    (["prodotti", "vendete"], "Sono innumerevoli i prodotti che vendiamo! Alimentari (caffè, tè, condimenti), articoli per la casa, cura del corpo, accessori e abbigliamento, borse e giochi/musica. Guarda qua! https://equocolibri.org+1", "all"),
    (["progetti", "supporto"], "I progetti sono l’essenza della Bottega. Ogni prodotto ha una storia a sé legata, pronta per essere raccontata. In vetrina troverai progetti come TRAME, BaSE Bangladesh, Naturveda, Libera Terra, Tatawelo, Smolart e altri; Scoprili nel link! https://equocolibri.org", "all"),
    (["commercio", "equo"], "Il commercio Equo e Solidale è un approccio alternativo al commercio che garantisce giustizia sociale, trasparenza, prezzi equi e sostenibilità, basato sui 10 principi del commercio equo. Scoprili tutti! https://equocolibri.org", "any"),
    (["riconoscere", "prodotto"], "Per riconoscere se un prodotto proviene dal commercio Equo è importante leggere le informazioni riportate sull’etichetta o sul sito del produttore. Controlla la presenza di certificazioni/loghi (Fairtrade, WFTO, ecc.), l’origine, la trasparenza della filiera e le informazioni sull’impatto sociale. https://equocolibri.org+1", "all"),
    (["certificazioni"], "Esistono alcune certificazioni importanti relative al commercio Equo: WFTO, Fairtrade, certificazione biologica e GOTS per il tessile; ogni certificazione ha criteri specifici. https://equocolibri.org", "any"),
    (["prezzo", "costo"], "Se pensi che i nostri prodotti costino di più, in realtà costano il Giusto! È un prezzo che riflette pagamenti equi ai produttori, reinvestimenti nelle comunità, materie prime di qualità e produzione artigianale; è un investimento etico! https://equocolibri.org", "all"),
    (["donazioni", "sostenere"], "Puoi sostenerci tramite tesseramento, acquisti abituali, partecipazione alle attività o collaborazioni; tutte le modalità sono descritte nel link https://equocolibri.org+1", "any"),
    (["tesseramento"], "La tessera annuale ha una quota di 20€ e offre uno sconto del 15% sui prodotti artigianali esposti (esclusi gli sconti già applicati). https://equocolibri.org", "any"),
    (["volontario", "diventare"], "Se vuoi diventare volontario passa in Bottega o contattaci su Instagram e verrai coinvolto in gestione negozio, eventi, laboratori, magazzino o comunicazione: accogliamo volontari di tutte le età. https://equocolibri.org+1", "all"),
    (["stage", "studenti"], "Se sei interessato ad un percorso di stage o servizio civile noi siamo a tua disposizione! Scrivici su Instagram oppure passa in Bottega. https://equocolibri.org", "any")
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower().strip()

    # Messaggio di benvenuto se l'utente non scrive nulla
    if user_message == "":
        welcome_msg = "Ciao! Benvenuto nella nostra chat 🐦. Posso raccontarti qualcosa sul commercio equo o sulla nostra bottega?"
        welcome_msg = re.sub(r"(https?://[^\s]+)", r'<a href="\1" target="_blank">\1</a>', welcome_msg)
        return jsonify({"reply": welcome_msg})

    reply = "Scusa, ma sto ancora imparando. Prova a riformulare la frase!"

    for keywords, answer, match_type in responses:
        if match_type == "all" and all(word in user_message for word in keywords):
            reply = answer
            break
        elif match_type == "any" and any(word in user_message for word in keywords):
            reply = answer
            break

    # Trasforma i link in cliccabili
    reply = re.sub(r"(https?://[^\s]+)", r'<a href="\1" target="_blank">\1</a>', reply)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
