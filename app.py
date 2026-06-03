from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Baca dataset
data = pd.read_csv("dataset.csv")


@app.route("/")
def home():
    return "AI Aktif"


@app.route("/recommend", methods=["POST"])
def recommend():

    input_user = request.json["bahan"].lower().strip()

    # sinonim
    input_user = input_user.replace("cabai", "cabe")

    bahan_dicari = input_user.split()

    results = []

    for _, hasil in data.iterrows():

        ingredients_text = str(
            hasil["ingredients"]
        ).lower()

        title_text = str(
            hasil["title"]
        ).lower()

        # pecah jadi kata
        kata_resep = (
            title_text.replace("|", " ").split()
            + ingredients_text.replace("|", " ").split()
        )

        jumlah_cocok = 0

        for bahan in bahan_dicari:

            if bahan in kata_resep:
                jumlah_cocok += 1

        # semua kata harus ditemukan
        if jumlah_cocok < len(bahan_dicari):
            continue

        score = round(
            (jumlah_cocok / len(bahan_dicari))
            * 100,
            2
        )

        results.append({
            "nama": str(hasil["title"]),
            "deskripsi": str(hasil["description"]),
            "kategori": str(hasil["category"]),
            "budget": int(hasil["budget"]),
            "waktu": int(hasil["time"]),
            "gambar": str(hasil["image"]),
            "bahan": str(hasil["ingredients"]),
            "langkah": str(hasil["steps"]),
            "score": score
        })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return jsonify(results[:5])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )