# Backend/app.py
import os, sys, sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from time import perf_counter


# import trie
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BACKEND_DIR)
sys.path.append(REPO_ROOT)
from Trie.trie_search import GameTrie
from heap.heap_search import *

DB_PATH = os.path.join(REPO_ROOT, "games_only.db")

# build trie once at startup
TRIE = GameTrie(max_top=10)
with sqlite3.connect(DB_PATH) as conn:
    rows = conn.execute(
        "SELECT appid, name FROM games WHERE name IS NOT NULL"
    ).fetchall()
    TRIE.build_from_rows(rows)

gamesList = read_games_from_db(DB_PATH)
trie = GameTrie().build((g.appid,g.name)for g in gamesList)
print(f"Loaded {len(gamesList)} games")

app = Flask(__name__)
CORS(app)  

@app.get("/search/trie")
def searchTrie():

    query = request.args.get("q","")
    limit = int(request.args.get("limit",100))

    start = perf_counter()
    results = trie.search(query,limit)
    finalTime = (perf_counter()-start)*1000

    gameLookup = {g.appid: g for g in gamesList}
    detailedGames = []
    for r in results:
        appid= r.get("appid")
        game = gameLookup.get(appid)
        if game:
             detailedGames.append({
                "appid": appid,"name": game.name,"price": getattr(game, "price", 0),
                "review_percent": getattr(game, "review_percent", None),"release_date": getattr(game, "release_date", "")
            })
        else:
             detailedGames.append({"appid": appid,"name": r.get("name", ""),
                                   "price": 0,"review_percent": None,"release_date": ""
            })
    return jsonify({"time_ms":round(finalTime,4),"results":detailedGames})






@app.get("/search/heap")
def searchHeap():

    sort_by = request.args.get("sort_by","")
    descending = True

    if sort_by in ("review_high", "price_high", "year_new"):
        descending = True
    elif sort_by in ("review_low", "price_low", "year_old"):
        descending = False

    limit = int(request.args.get("limit",10))

    map = {"review_high": "review_percent","review_low": "review_percent","price_high": "price",
            "price_low": "price", "year_new": "release_date", "year_old": "release_date",
    }

    sorting_key= map.get(sort_by,"review_percent") 


    start = perf_counter()
    heap = build_heap(gamesList,sort_by=sorting_key,descending=descending)
    results = extract_top_n(heap,limit)
    finalTime= (perf_counter()-start)*1000
    return jsonify({
        "time_ms": round(finalTime, 4),
        "results": [
            {"appid": g.appid,"name": g.name,"price": getattr(g, "price", 0),
                "review_percent": getattr(g, "review_percent", None),"release_date": getattr(g, "release_date", "")
            }
            for g in results
        ]
    })


if __name__ == "__main__":
    app.run(debug=False)  
