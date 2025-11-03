
import re
import unicodedata #removes accents
from typing import Iterable, List, Tuple, Optional, Dict, Set


class TrieNode:
    __slots__ = ("children", "end_ids", "top", "_top_set")
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.end_ids: Set[int] = set()
        self.top: List[Dict[str, object]] = []  
        self._top_set: Set[int] = set()          


class GameTrie:
    def __init__(self, max_top: int = 10):
        self.root = TrieNode()
        self.max_top = max_top
        self._seen: Set[int] = set()
        self._names: Dict[int, str] = {}

    # removes accents
    @staticmethod
    def _ascii_fold(s: str) -> str:
        nkfd = unicodedata.normalize("NFKD", s)
        return "".join(ch for ch in nkfd if not unicodedata.combining(ch))

    #turns all to lowercase and replaces special characters with spaces
    @staticmethod
    def normalize_title(raw: str, fold: bool = True) -> str:
        s = raw.lower()
        if fold:
            s = GameTrie._ascii_fold(s)
        # keep letters/digits, replace the rest with single spaces
        s = re.sub(r"[^a-z0-9]+", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s


    #indexes every new word allowing searches to start from any word in title
    @staticmethod
    def _word_starts(s: str) -> List[int]:
        if not s:
            return []
        idx = [0]
        for i in range(1, len(s)):
            if s[i - 1] == " " and s[i] != " ":
                idx.append(i)
        return idx

    # adds entry to suggestions list if list is below the size of max_top
    def _maybe_push_top(self, node: TrieNode, appid: int, name: str) -> None:

        if appid in node._top_set:
            return
        if len(node.top) < self.max_top:
            node.top.append({"appid": appid, "name": name})
            node._top_set.add(appid)

    # inserts a string from 
    def _insert_from_pos(self, s: str, pos: int, appid: int, name: str) -> None:
        node = self.root
        self._maybe_push_top(node, appid, name)

        for ch in s[pos:]:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            self._maybe_push_top(node, appid, name)

        node.end_ids.add(appid)

    
    def insert(self, appid: int, name: str, fold: bool = True) -> None:
        if appid in self._seen:
            return
        norm = self.normalize_title(name, fold=fold)
        if not norm:
            return
        for pos in self._word_starts(norm):
            self._insert_from_pos(norm, pos, appid, name)
        self._seen.add(appid)
        self._names[appid] = name

    def build(self, games: Iterable[Tuple[int, str]]) -> "GameTrie":
        return self.build_from_rows(games)

    def build_from_rows(self, rows: Iterable[Tuple[int, str]]) -> "GameTrie":
        for appid, name in rows:
            self.insert(appid, name)
        return self

    def _walk(self, prefix: str) -> Optional[TrieNode]:
        s = self.normalize_title(prefix)
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, prefix: str, limit: int = 10) -> List[Dict[str, object]]:

        if not prefix or prefix.strip() == "":
            return self.root.top[:limit]

        node = self._walk(prefix)
        if node is None:
            return []

        if len(node.top) >= limit:
            return node.top[:limit]

        results = list(node.top)
        seen = {r["appid"] for r in results}

        stack = list(node.children.values())
        while stack and len(results) < limit:
            cur = stack.pop()
            for e in cur.top:
                aid = e["appid"]
                if aid not in seen:
                    results.append(e)
                    seen.add(aid)
                    if len(results) >= limit:
                        break
            stack.extend(cur.children.values())

        return results[:limit]
