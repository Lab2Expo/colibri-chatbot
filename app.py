import os
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Lista FAQ: parole chiave + risposta + tipo matching ("all" o "any")
responses = [
    (["bottega", "dove siete", "indirizzo", "dove", "monselice"], 
 "Puoi trovare la nostra Bottega in centro a Monselice in Via Roma 26, Monselice (PD) — 35043 https://www.equocolibri.org/contattaci.html", 
 "any"),

(["ciao", "buongiorno", "buonsera"], 
 "Ciao, sono Il Colibrì. Fammi qualche domanda e proverò a risponderti!", 
 "any"),

(["orari", "apertura", "aperti", "giorni", "orario"], 
 "Solitamente i giorni di apertura sono : lunedì, mercoledì, giovedì, venerdì e sabato 9:30–12:00 e 15:30–19:00; Puoi anche contattarci direttamente su instagram! https://www.instagram.com/ilcolibri.monselice/", 
 "any"),

(["contattare", "informazioni", "scrivere", "chiedere", "domande", "instagram", "bisogno"], 
 "Se vuoi informazioni di qualunque genere scrivici su instagram! https://www.instagram.com/ilcolibri.monselice/", 
 "any"),

(["online", "negozio online", "ecommerce", "comprare su internet", "vendita online"], 
 "Non abbiamo un negozio on line perchè per noi è importante comunicare direttamente al cliente. In Bottega potrai fare un viaggio nel mondo del commercio Equo.", 
 "any"),

(["prodotti", "cosa vendete", "cosa trovo", "alimentari", "articoli", "proposte"], 
 "Sono innumerevoli i prodotti che vendiamo! Alimentari (caffè, tè, condimenti), articoli per la casa, cura del corpo, accessori e abbigliamento, borse e giochi/musica. Guarda qua! https://www.equocolibri.org/alimentari1.html", 
 "any"),

(["progetti", "cosa sostenete", "iniziative", "storie prodotti", "marchi"], 
 "I progetti sono l’essenza della Bottega. Ogni prodotto ha una storia a sé legata, pronta per essere raccontata. In vetrina troverai progetti come TRAME, BaSE Bangladesh, Naturveda, Libera Terra, Tatawelo, Smolart e altri; Scoprili nel link! https://www.equocolibri.org/progetti-equo-e-solidali.html", 
 "any"),

(["commercio equo", "cosa significa equo", "definizione commercio equo", "principi commercio equo", "significato"], 
 "Il commercio Equo e Solidale è un approccio alternativo al commercio che garantisce giustizia sociale, trasparenza, prezzi equi e sostenibilità, basato sui 10 principi del commercio equo. Scoprili tutti! https://www.equocolibri.org/commercioequoesolidale.html", 
 "any"),

(["come riconoscere prodotti equo", "etichette", "loghi equo", "certificazioni", "filiera trasparente", "riconoscere"], 
 "Per riconoscere se un prodotto proviene dal commercio Equo è importante leggere le informazioni riportate sull'etichetta o sul sito del produttore. Controlla la presenza di certificazioni/loghi (Fairtrade, WFTO, ecc.), l’origine, la trasparenza della filiera e le informazioni sull’impatto sociale. https://www.equocolibri.org/come-identificare-i-prodotti-del-commercio-equo-e-solidale.html", 
 "any"),

(["certificazioni", "fairtrade", "wfto", "biologico", "gots"], 
 "Esistono alcune certificazioni importanti relative al commercio Equo: WFTO, Fairtrade, certificazione biologica e GOTS per il tessile; ogni certificazione ha criteri specifici. https://www.equocolibri.org/le-certificazioni.html", 
 "any"),

(["prezzi", "quanto costa", "perché costa di più", "prezzi equi", "giusto prezzo"], 
 "Se pensi che i nostri prodotti costino di più, in realtà costano il Giusto! E' un prezzo che riflette pagamenti equi ai produttori, reinvestimenti nelle comunità, materie prime di qualità e produzione artigianale; è un investimento etico! https://www.equocolibri.org/i-prezzi-trasp8203arenti-del-commercio-equo-e-solidale.html", 
 "any"),

(["aiuto", "cosa posso fare", "sostenere", "collaborare", "tesseramento"], 
 "Cosa puoi fare per noi? Puoi sostenerci tramite tesseramento, acquisti abituali, partecipazione alle attività o collaborazioni; tutte le modalità sono descritte nel link https://www.equocolibri.org/partecipa.html", 
 "any"),

(["tessera", "costo tessera", "quanto costa", "quota associativa", "sconto"], 
 "La tessera annuale ha una quota di 20€ e offre uno sconto del 15% sui prodotti artigianali esposti (esclusi gli sconti già applicati). https://www.equocolibri.org/partecipa.html", 
 "any"),

(["volontario", "aiutare in bottega", "diventare volontario", "collaborare", "volontariato"], 
 "Se vuoi diventare volontario passa in Bottega o Contattaci in instagram e verrai coinvolto in gestione negozio, eventi, laboratori, magazzino o comunicazione: accogliamo volontari di tutte le età. https://www.equocolibri.org/partecipa.html", 
 "any"),

(["stage", "servizio civile", "tirocinio", "fare esperienza", "alternanza scuola lavoro"], 
 "Se sei interessato ad un percorso di stage o servizio civile noi siamo a tua disposizione! Scrivici su instagram oppure passa in Bottega. https://www.instagram.com/ilcolibri.monselice/", 
 "any"),

(["eventi", "laboratori", "scuole", "iniziative", "collaborazioni"], 
 "Se sei interessato possiamo organizzare e co-progettare eventi, incontri e laboratori; anche con le scuole! Scrivici su instagram e iniziamo a collaborare! https://www.instagram.com/ilcolibri.monselice/", 
 "any"),

(["materiale informativo", "informazioni", "approfondimenti", "libri", "documenti"], 
 "Se sei in cerca di materiale informativo sul sito trovi pagine di approfondimento (filiera, certificazioni, temi come gender gap e prezzi trasparenti). In Bottega abbiamo anche tanti libri che potrebbero fare al caso tuo!", 
 "any"),

(["associazione", "statuto", "presidente", "consiglio direttivo", "iscritta"], 
 "Siamo un’associazione di volontariato iscritta al registro comunale delle Associazioni di volontariato, all'elenco regionale e all'AGICES; abbiamo uno statuto, un Presidente e un Consiglio Direttivo. https://www.equocolibri.org/organizzazione.html", 
 "any"),

(["gestione", "chi siete", "chi lavora", "volontari", "storia bottega"], 
 "La Bottega è gestita interamente da volontari dell'Associazione “Il Colibrì - tutti i colori del mondo” che credono nella diffusione di un Commercio Giusto già dal 2004 https://www.equocolibri.org/la-nosta-storia.html", 
 "any"),

(["10 principi", "principi commercio equo", "uguaglianza", "sostenibilità", "no sfruttamento"], 
 "Se parliamo dei 10 principi allora stiamo parlando di creazione di opportunità per produttori svantaggiati, trasparenza, pagamenti equi, assenza di sfruttamento minorile, uguaglianza di genere e sostenibilità ambientale. Scoprili nel dettaglio qui https://www.equocolibri.org/commercioequoesolidale.html", 
 "any"),

(["socio", "diventare socio", "vantaggi socio", "tessera socio", "sconto socio"], 
 "Se diventi nostro socio puoi usufruire di uno sconto del 15% sui prodotti artigianali esposti (esclusi gli sconti già applicati). https://www.equocolibri.org/partecipa.html", 
 "any"),

(["gas", "gruppo acquisto solidale", "acquisto collettivo", "spesa etica", "gruppi di acquisto"], 
 "Collaboriamo con diversi GAS (Gruppi di Acquisto Solidale) della zona: sono realtà che scelgono di acquistare collettivamente prodotti etici e sostenibili. Vuoi info per il tuo GAS? Scrivici! https://www.equocolibri.org/contatti.html", 
 "any"),

([ "fairtrade", "Fairtade", "wfto", "marchio", "garanzia"], 
 "I prodotti in Bottega seguono diversi sistemi di garanzia: WFTO, Fairtrade e altre certificazioni indipendenti. Tutte hanno lo scopo di tutelare i produttori e garantire trasparenza. https://www.equocolibri.org/commercioequoesolidale.html", 
 "any"),

(["produttori", "cooperative", "artigiani", "paesi del sud", "partner"], 
 "Lavoriamo con cooperative di produttori in Asia, Africa e America Latina, oltre a progetti sociali in Italia. Ognuno di loro riceve un compenso equo e opportunità di sviluppo. https://www.equocolibri.org/produttori.html", 
 "any"),


(["donazione", "offerta", "sostegno economico", "aiuto economico", "5x1000"], 
 "Puoi sostenerci anche con donazioni o destinando il tuo 5x1000. Trovi le modalità indicate qui: https://www.equocolibri.org/partecipa.html", 
 "any"),


(["cibo", "cioccolato", "caffè", "tè", "alimentari"], 
 "La sezione alimentare della Bottega offre caffè, tè, cacao, cioccolato, zucchero e molto altro: tutti prodotti da filiere trasparenti e senza sfruttamento. https://www.equocolibri.org/prodotti.html", 
 "any"),

(["artigianato", "borse", "gioielli", "casa", "decorazioni"], 
 "Abbiamo tanti prodotti di artigianato da Asia, Africa e America Latina: borse, gioielli, tessili, accessori e oggetti per la casa. https://www.equocolibri.org/prodotti.html", 
 "any"),

(["scuola", "insegnanti", "studenti", "progetti educativi", "laboratori scuola"], 
 "Proponiamo laboratori e percorsi educativi per scuole di ogni ordine e grado su commercio equo, sostenibilità e cittadinanza globale. https://www.equocolibri.org/scuole.html", 
 "any"),

(["campagna", "attivismo", "petizione", "locali", "territorio"], 
 "Il Colibrì non è solo Bottega: partecipiamo a campagne di sensibilizzazione e azioni di attivismo sul territorio 🌍 Seguici per restare aggiornato! https://www.instagram.com/ilcolibri.monselice/", 
 "any"),

(["cooperativa", "associazione", "chi siete", "storia", "colibrì"], 
 "Il Colibrì è un’associazione di volontariato che promuove il commercio equo e solidale, la sostenibilità e la giustizia sociale. Scopri la nostra storia qui: https://www.equocolibri.org/chi-siamo.html", 
 "any"),

(["eventi", "organizzate", "serate", "incontri", "attività"], 
 "Organizziamo eventi, incontri culturali, serate a tema e attività di sensibilizzazione sul territorio 🌱 Consulta il calendario: https://www.equocolibri.org/eventi.html", 
 "any"),

(["sostenibilità", "ambiente", "ecologia", "green", "clima"], 
 "Crediamo nella sostenibilità ambientale: i nostri prodotti rispettano la natura e sostengono filiere responsabili 🌍 https://www.equocolibri.org/valori.html", 
 "any"),

(["trasparenza", "filiera", "origine", "chi produce", "da dove viene"], 
 "Ogni prodotto ha una storia chiara e trasparente: conosci l’origine, chi lo produce e come viene distribuito. https://www.equocolibri.org/prodotti.html", 
 "any"),

(["solidale", "giustizia sociale", "diritti", "uguaglianza", "etico"], 
 "Il commercio equo e solidale si fonda su giustizia sociale, diritti rispettati e uguaglianza tra produttori e consumatori. https://www.equocolibri.org/commercioequoesolidale.html", 
 "any"),

(["corsi", "formazione", "workshop", "laboratori", "esperienze"], 
 "Proponiamo workshop e laboratori di formazione su consumo critico, commercio equo e cittadinanza attiva. https://www.equocolibri.org/laboratori.html", 
 "any"),

(["bottega online", "acquistare online", "shop", "e-commerce", "vendita online"], 
 "Non abbiamo un e-commerce perché crediamo nel valore del contatto diretto con le persone 💬 Vieni a trovarci in Bottega! https://www.equocolibri.org/prodotti.html", 
 "any"),

(["gastronomia", "spezie", "olio", "pasta", "vino"], 
 "Oltre al caffè e al cioccolato trovi anche pasta, riso, olio, vino e spezie da filiere etiche e sostenibili 🍷 https://www.equocolibri.org/prodotti.html", 
 "any"),

(["volontariato", "aiutare", "dare una mano", "tempo libero", "collaborare"], 
 "Il volontariato è il cuore del Colibrì 💛 Puoi dare una mano in Bottega, negli eventi o nella comunicazione. Info qui: https://www.equocolibri.org/partecipa.html", 
 "any"),

(["rete", "collaborazioni", "altre associazioni", "partner locali", "territorio"], 
 "Facciamo parte di una rete di associazioni e realtà locali che condividono i nostri stessi valori ✨ https://www.equocolibri.org/chi-siamo.html", 
 "any"),

(["bomboniere", "regali", "forniture", "personalizzato", "su richiesta"], 
 "Possiamo realizzare bomboniere e forniture personalizzate e regali : contattaci in Bottega per dettagli e preventivi 🎁", 
 "any"),

(["giochi", "bambini", "piccoli", "educativi", "musica"], 
 "Abbiamo anche una sezione dedicata ai più piccoli: giochi, libri e musica equo-solidale per crescere con valori giusti 👶🎶", 
 "any"),

(["donne", "femminile", "parità di genere", "empowerment", "gender gap"], 
 "L’empowerment femminile è un tema fondamentale per noi 🌸 Approfondisci qui: https://www.equocolibri.org/donne-nel-commercio-equo.html", 
 "any"),

(["campagne", "territorio", "territoriali", "iniziative locali", "buzzaccarini"], 
 "Partecipiamo attivamente a campagne territoriali e collaboriamo con realtà locali come il Parco Buzzaccarini 🌳", 
 "any"),

(["prezzi", "trasparenti", "margini", "costi", "perché costa"], 
 "I nostri prezzi sono trasparenti e raccontano un percorso di equità e sostenibilità 💶 https://www.equocolibri.org/i-prezzi-trasp8203arenti-del-commercio-equo-e-solidale.html", 
 "any"),

(["storia", "nascita", "fondazione", "2004", "origini"], 
 "Il Colibrì nasce nel 2004 dall’incontro di studenti e donne attive sul territorio ✨ Scopri di più: https://www.equocolibri.org/la-nosta-storia.html", 
 "any"),

(["donazioni", "ricavato", "sostenere progetti", "aiuto", "solidarietà"], 
 "Parte del ricavato sostiene progetti equo-solidali e attività locali, oltre a donazioni annuali verso paesi in difficoltà 🌍", 
 "any"),

(["social", "facebook", "instagram", "seguici", "aggiornamenti"], 
 "Seguici su Instagram e Facebook per restare aggiornato su eventi, notizie e prodotti 👉 https://www.instagram.com/ilcolibri.monselice/", 
 "any"),

(["problemi", "assistenza", "supporto", "aiuto", "informazioni"], 
 "Se hai avuto un problema con un prodotto o vuoi chiarimenti, scrivici subito sui nostri social 💬 https://www.equocolibri.org/partecipa.html", 
 "any"),

(["novità", "forum", "news", "aggiornato"], 
 "Per rimanere sempre aggiornato visita la sezione 'Eventi e News' e i nostri social 📌 https://www.equocolibri.org/partecipa.html", 
 "any"),

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
