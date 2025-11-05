
#This reads the db and builds the heap, adjust the db filepath on line 79 (in the main function)

import sqlite3
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

class Heap:
    def __init__(self, key_func, descending=False):
        self.data = []
        self.key_func = key_func
        self.descending = descending
        self.counter = itertools.count()

    def _compare(self, a, b):
        # Returns True if a should be above b in heap
        if self.descending:
            return a[0] > b[0]  # max-heap
        else:
            return a[0] < b[0]  # min-heap

    def push(self, item):
        key = self.key_func(item)
        count = next(self.counter)
        node = (key, count, item)
        self.data.append(node)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            raise IndexError("pop from empty heap")

        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)

        return top[2]

    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        while idx > 0 and self._compare(self.data[idx], self.data[parent]):
            self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        n = len(self.data)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            best = idx

            if left < n and self._compare(self.data[left], self.data[best]):
                best = left
            if right < n and self._compare(self.data[right], self.data[best]):
                best = right

            if best == idx:
                break
            self.data[idx], self.data[best] = self.data[best], self.data[idx]
            idx = best

    def __len__(self):
        return len(self.data)


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
        cursor.execute("SELECT appid, name, price, release_date FROM steam_apps;")
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
    if sort_by == "price":
        key_func = lambda g: g.price
    else:
        key_func = lambda g: date_to_int(g.release_date)

    heap = Heap(key_func, descending=descending)
    for g in games:
        heap.push(g)
    return heap


def extract_top_n(heap: Heap, n: int):
    result = []
    for _ in range(n):
        if len(heap) == 0:
            break
        result.append(heap.pop())
    return result


# Example
if __name__ == "__main__":

    # adjust the dathpath of the db file here
    db_path = "toy.db"



    games = read_games_from_db(db_path)

    if not games:
        print("No games found in database.")
    else:
        print(f"Loaded {len(games)} games from {db_path}")

        # Ex: release date descending
        heap = build_heap(games, sort_by="price", descending=True)
        top_games = extract_top_n(heap, 5)

        print("\nTop 5 most recent games:")
        for g in top_games:
            print(f"- {g.name} : price ${g.price}")

