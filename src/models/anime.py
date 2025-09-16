from dataclasses import dataclass, field
from typing import List



@dataclass
class PartialAnime:
    id: int
    title: str
    score: float
    episodes: int



@dataclass
class Anime:
    id: int
    title: str
    synopsis: str
    episodes: int
    score: float
    genres: List[str] = field(default_factory=List[str])