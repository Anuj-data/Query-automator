from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ── Language Codes ───────────────────────────────────────────────────────────
lang_codes = {
    "english":   "en",
    "hindi":     "hi",
    "bengali":   "bn",
    "gujarati":  "gu",
    "marathi":   "mr",
    "punjabi":   "pa",
    "tamil":     "ta",
    "telugu":    "te",
    "kannada":   "kn",
    "malayalam": "ml",
    "urdu":      "ur"
}

# ── Cache ─────────────────────────────────────────────────────────────────────
transliteration_cache = {}

# ── Transliteration Function (Google Input Tools — No API key needed) ─────────
def transliterate_word(word, lang_code):
    """
    Phonetic transliteration using Google Input Tools.
    'energy' → 'एनर्जी' (NOT 'ऊर्जा')
    'Airtel' → 'एयरटेल' (NOT 'वायुसेना')
    """
    cache_key = f"{word}_{lang_code}"
    if cache_key in transliteration_cache:
        return transliteration_cache[cache_key]

    try:
        url = "https://inputtools.google.com/request"
        params = {
            "text": word,
            "itc":  f"{lang_code}-t-i0-und",
            "num":  1
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()

        if result[0] == "SUCCESS":
            transliterated = result[1][0][1][0]
            transliteration_cache[cache_key] = transliterated
            return transliterated

        return word

    except Exception as e:
        print(f"[Transliteration ERROR] word='{word}', lang='{lang_code}', error={e}")
        return word


def transliterate_text(text, lang_code):
    """
    Transliterate each word in the text separately, then join.
    'Ather Energy' → 'एथर एनर्जी'
    """
    words = text.split()
    transliterated_words = [transliterate_word(w, lang_code) for w in words]
    return " ".join(transliterated_words)


# ── Generate Variations ───────────────────────────────────────────────────────
def generate_variations(keyword, selected_languages):
    variations = set()

    for lang in selected_languages:
        code = lang_codes.get(lang.lower())

        if code == "en":
            # English — exactly as user typed
            variations.add(keyword)
        elif code:
            # Other language — phonetic transliteration
            transliterated = transliterate_text(keyword, code)
            if transliterated:
                variations.add(transliterated)

    return list(variations)


# ── Query Builder ─────────────────────────────────────────────────────────────
def build_query(keywords, operator, selected_languages):
    all_parts = []
    for keyword in keywords:
        variations = generate_variations(keyword, selected_languages)
        escaped_vars = [f'"{v}"' for v in variations]
        part = " OR ".join(escaped_vars)
        all_parts.append(f"({part})")
    return f" {operator} ".join(all_parts)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        keywords_input = data.get("keyword", "")
        operator       = data.get("operator", "AND")
        languages      = data.get("languages", ["english"])

        keywords_list = [k.strip() for k in keywords_input.split(",") if k.strip()]

        if not keywords_list:
            return jsonify({"error": "No keywords provided", "query": ""})

        query = build_query(keywords_list, operator, languages)

        return jsonify({"query": query, "raw_query": query})

    except Exception as e:
        print(f"[Generate ERROR] {e}")
        return jsonify({"error": str(e), "query": "Error generating query"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)