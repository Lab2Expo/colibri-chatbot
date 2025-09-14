from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

responses = {
    "ciao": "Ciao! Sono il Colibrì 🌱, benvenuto nel nostro mondo di commercio equo e solidale!",
    "commercio": "Il commercio equo sostiene i produttori del Sud del mondo garantendo un prezzo giusto, diritti per i lavoratori e rispetto per l’ambiente.",
    "prodotti": "Vendiamo cibo, artigianato e tessili dal commercio equo, bio e solidali.",
    "dove": "Siamo a Monselice, in via … Ti aspettiamo!",
    "volontario": "Certo! Puoi contattarci o passare in bottega: ogni aiuto fa la differenza.",
    "perchè": "Ogni acquisto sostiene comunità e progetti di giustizia sociale."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()

    reply = "Non ho capito bene 🤔, ma posso raccontarti del commercio equo se vuoi!"
    for key in responses:
        if key in user_message:
            reply = responses[key]
            break

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
