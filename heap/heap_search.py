
#This reads the db and builds the heap, adjust the db filepath on line 79 (in the main function)

import sqlite3
import heapq
from datetime import datetime
from dataclasses import dataclass
from typing import List
import itertools

@dataclass
class Game:
    appid: int
    name: str
    price: float
    release_date: str


# "Nov 1, 2000" → 20001101
def date_to_int(date_str: str) -> int:
    try:
        dt = datetime.strptime(date_str, "%b %d, %Y")
        return dt.year * 10000 + dt.month * 100 + dt.day
    except ValueError:
        return 0


def read_games_from_db(db_path: str) -> List[Game]:
    games = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT appid, name, price, release_date FROM games;")
        rows = cursor.fetchall()

        for row in rows:
            appid, name, price, release_date = row
            games.append(Game(appid=appid, name=name, price=price, release_date=release_date))
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

    return games


def build_heap(games: List[Game], sort_by: str = "price", descending: bool = False):

    def floatify(x):
        try: 
            return float(x)
        except (TypeError,ValueError):
            return 0.0



    if sort_by == "price":
        key_func = lambda g: floatify(getattr(g,g.price,0))
    elif sort_by == "release_date":
        key_func = lambda g: date_to_int(g.release_date)
    elif sort_by == "review_percent":
        key_func = lambda g: floatify(getattr(g, "review_percent", 0))
    else:
        key_func = lambda g: 0
        

    counter = itertools.count()

    # for descending, negate key
    if descending:
        heap = [(-key_func(g), next(counter), g) for g in games]
    else:
        heap = [(key_func(g), next(counter), g) for g in games]

    heapq.heapify(heap)
    return heap


def extract_top_n(heap, n: int):
    result = []
    for _ in range(n):
        if not heap:
            break
        _, _, game = heapq.heappop(heap)
        result.append(game)
    return result


# Example
if __name__ == "__main__":

    # adjust the dathpath of the db file here
    db_path = "./games_only.db"



    games = read_games_from_db(db_path)

    if not games:
        print("No games found in database.")
    else:
        print(f"Loaded {len(games)} games from {db_path}")

        # Ex: release date descending
        heap = build_heap(games, sort_by="release_date", descending=True)
        top_games = extract_top_n(heap, 5)

        print("\nTop 5 most recent games:")
        for g in top_games:
            print(f"- {g.name}: released {g.release_date}")

