# Backend/app.py
import os, sys, sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

# import trie
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BACKEND_DIR)
sys.path.append(REPO_ROOT)
from Trie.trie_search import GameTrie


DB_PATH = os.path.join(REPO_ROOT, "toy.db")

# build trie once at startup
TRIE = GameTrie(max_top=10)
with sqlite3.connect(DB_PATH) as conn:
    rows = conn.execute(
        "SELECT appid, name FROM steam_apps WHERE name IS NOT NULL"
    ).fetchall()
    TRIE.build_from_rows(rows)


app = Flask(__name__)
CORS(app)  

@app.get("/api/search")
def search():
    q = request.args.get("q", "", type=str)
    limit = request.args.get("limit", 10, type=int)
    return jsonify(TRIE.search(q, limit=limit))

if __name__ == "__main__":
    app.run(debug=False)  
