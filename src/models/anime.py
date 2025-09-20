from dataclasses import dataclass, field
from operator import ge
from typing import List, Any, Dict, Optional, Union
from datetime import datetime, timedelta

@dataclass
class Themes:
    openings: Optional[List[str]]
    endings: Optional[List[str]]

@dataclass
class Airing: 
    start: Optional[datetime]
    stop: Optional[datetime]

@dataclass
class Title:
    main: str
    english: str
    japanese: str 
    alternatives: List[str] = field(default_factory=List[str])

@dataclass
class Genre:
    id: int
    name: str

class Statistic:
    ...

class Recommendation:
    ... # maybe sames as PartialAnime?

@dataclass
class MainPictures:
    medium: str
    large: str

@dataclass
class Studio:
    id: int
    name: str

@dataclass
class PartialAnime:
    id: int
    title: Title
    airing: Airing
    synopsis: str
    mean: float
    rank: Optional[int]
    popularity: Optional[int]
    score: Optional[float]
    episodes: Optional[int]
    nsfw: str
    created_at: datetime
    updated_at: Optional[datetime]
    media_type: str
    status: str
    genres: List[Genre]
    source: Optional[str]
    average_episode_duration: Optional[timedelta]
    rating: Optional[str]
    studios: List[Studio]
    main_pictures: MainPictures




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
    rank: Optional[int]
    source: Optional[str]
    status: str
    airing: Airing
    image_url: str
    statistics: Dict[str, Union[Dict[str, str], str, int]]
    recommendations: Optional[List[Dict[str, Dict[str, str]]]]
    title_synopsis: List[str] = field(default_factory=List[str])

