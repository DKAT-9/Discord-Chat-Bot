from __future__ import annotations
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

STOPWORDS = {"the", "a", "an", "is", "are", "to", "and", "of", "in", "on", "for", "my", "your"}

def _tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-z0-9/]+", text.lower())
    return [w for w in words if w not in STOPWORDS]

@dataclass
class KBEntry:
    id: str
    tags: List[str]
    question: str
    answer: str

class KnowledgeBase:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.entries: List[KBEntry] = []
        self._load()

    def _load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.entries = [
            KBEntry(
                id=e["id"],
                tags=e.get("tags", []),
                question=e["question"],
                answer=e["answer"],
            )
            for e in raw.get("entries", [])
        ]

    def search(self, user_text: str) -> Optional[Tuple[KBEntry, float]]:
        """Return best match with a simple token overlap score."""
        # Reload knowledge base from disk on each search
        self._load()
        
        q_tokens = set(_tokenize(user_text))
        if not q_tokens:
            return None

        best: Optional[Tuple[KBEntry, float]] = None
        for entry in self.entries:
            hay = " ".join([entry.question, " ".join(entry.tags)])
            e_tokens = set(_tokenize(hay))
            overlap = len(q_tokens & e_tokens)
            denom = max(1, len(q_tokens))
            score = overlap / denom  # 0..1

            if best is None or score > best[1]:
                best = (entry, score)

        if best and best[1] >= 0.25:
            return best
        return None