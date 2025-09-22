from dataclasses import dataclass, field
from operator import ge
from typing import List, Any, Dict, Literal, Optional, Union
from datetime import datetime, timedelta
from dataclasses_json import dataclass_json, config


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

@dataclass
class Status:
    watching: str
    completed: str
    on_hold: str
    dropped: str
    plan_to_watch: str

    @property
    def completion_rate(self) -> Optional[float]:
        """
        returns the completion rate between 0 and 1
        which sums up watching, completed, on_hold and dropped
        """
        try:
            user_amount = sum([int(self.watching), int(self.completed), int(self.completed), int(self.on_hold)])
            return int(self.completed) / user_amount
        except Exception:
            return None

@dataclass
class Statistic:
    status: Status
    num_list_users: int


@dataclass
class Song:
    id: int
    anime_id: int
    text: str


@dataclass_json
@dataclass
class Picture:
    medium: str
    large: str


@dataclass_json
@dataclass
class Studio:
    id: int
    name: str


@dataclass_json
@dataclass
class MinimalAnime:
    id: int
    title: str
    main_picture: Picture


@dataclass_json
@dataclass
class RelatedAnime:
    anime: MinimalAnime = field(metadata=config(field_name="node"))
    replation_type: Literal["prequel", "sequel", "alternative_setting", "alternative_version", "side_story", "summary", "parent_story", "spin_off"]
    relation_type_formatted: str


@dataclass_json
@dataclass
class Recommendation:
    anime: MinimalAnime = field(metadata=config(field_name="node"))
    num_recommendations: int


@dataclass
class PartialAnime(MinimalAnime):
    """
    Represents an anime from MyAnimeList fetched with the 
    search, which does not contain all information.
    """
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
    main_pictures: List[Picture]


@dataclass
class Anime(PartialAnime):
    """
    Represents an anime from MyAnimeList with complete information fetched by ID.
    """
    pictures: List[Picture]
    background: Optional[str]
    related_anime: List[RelatedAnime]
    recommendations: List[Recommendation]
    opening_themes: List[Song]
    ending_themes: List[Song]



