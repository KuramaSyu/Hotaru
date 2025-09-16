from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional, Union
from datetime import datetime

@dataclass
class Themes:
    openings: Optional[List[str]]
    endings: Optional[List[str]]

class Airing: 
    start: Optional[datetime]
    stop: Optional[datetime]

@dataclass
class Title:
    main: str
    english: str
    japanese: str 

@dataclass
class PartialAnime:
    id: int
    title: Title
    score: Optional[float]
    episodes: Optional[int]



# Todo: check mal response and add classes 
@dataclass
class Anime(PartialAnime):
    id: int
    title: Title
    synopsis: str
    score: Optional[float]
    popularity: Optional[int]
    related: Dict[str, List[Dict[str, Any]]]
    themes: Themes
    rating: str
    rank: Optional[int]
    source: Optional[str]
    status: str
    airing: Airing
    image_url: str
    studios: List[Dict[str, str]]

    genres: List[Dict[str, str]]
    statistics: Dict[str, Union[Dict[str, str], str, int]]
    recommendations: Optional[List[Dict[str, Dict[str, str]]]]
    title_synopsis: List[str] = field(default_factory=List[str])


class Genre:
    ...

class Statistic:
    ...

class Recommendation:
    ... # maybe sames as PartialAnime?

class Studio:
    ...