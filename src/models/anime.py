from dataclasses import dataclass, field
from operator import ge
from typing import List, Any, Dict, Literal, Optional, Union
from datetime import datetime, timedelta
from dataclasses_json import DataClassJsonMixin, dataclass_json, config

iso_datetime_no_optional_config = config(
    decoder=datetime.fromisoformat,
    encoder=lambda date: date.isoformat()
)
iso_datetime_config = config(
    decoder=lambda date: datetime.fromisoformat(date) if date else None,
    encoder=lambda date: date.isoformat() if date else None,
)

@dataclass
class Themes(DataClassJsonMixin):
    openings: Optional[List[str]]
    endings: Optional[List[str]]

@dataclass
class Title:
    main: str
    english: str
    japanese: str 
    alternatives: List[str] = field(default_factory=List[str])

@dataclass
class Genre(DataClassJsonMixin):
    id: int
    name: str

@dataclass
class Status(DataClassJsonMixin):
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
class Statistic(DataClassJsonMixin):
    status: Status
    num_list_users: int

@dataclass
class Song(DataClassJsonMixin):
    id: int
    anime_id: int
    text: str


@dataclass
class Picture(DataClassJsonMixin):
    medium: str
    large: str


@dataclass
class Studio(DataClassJsonMixin):
    id: int
    name: str


@dataclass
class MinimalAnime(DataClassJsonMixin):
    id: int
    title: str
    main_picture: Picture


@dataclass
class RelatedAnime(DataClassJsonMixin):
    anime: MinimalAnime = field(metadata=config(field_name="node"))
    relation_type: Literal["prequel", "sequel", "alternative_setting", "alternative_version", "side_story", "summary", "parent_story", "spin_off"]
    relation_type_formatted: str


@dataclass
class Recommendation(DataClassJsonMixin):
    anime: MinimalAnime = field(metadata=config(field_name="node"))
    num_recommendations: int


@dataclass
class PartialAnime(MinimalAnime, DataClassJsonMixin):
    """
    Represents an anime from MyAnimeList fetched with the 
    search, which does not contain all information.
    """
    synopsis: str
    nsfw: str
    media_type: str
    status: str
    genres: List[Genre]
    average_episode_duration: Optional[timedelta]
    studios: List[Studio]
    main_picture: Picture
    created_at: datetime = field(metadata=iso_datetime_no_optional_config)
    
    mean: Optional[float] = None
    start_date: Optional[datetime] = field(metadata=iso_datetime_config, default_factory=lambda: None)
    end_date: Optional[datetime] = field(metadata=iso_datetime_config, default_factory=lambda: None)
    source: Optional[str] = None
    updated_at: Optional[datetime] = field(metadata=iso_datetime_config, default_factory=lambda: None)
    rating: Optional[str] = None
    rank: Optional[int] = None
    popularity: Optional[int] = None
    num_episodes: Optional[int] = None

@dataclass
class Anime(PartialAnime, DataClassJsonMixin):
    """
    Represents an anime from MyAnimeList with complete information fetched by ID.
    """
    pictures: List[Picture] = field(default_factory=list[Picture])
    related_anime: List[RelatedAnime] = field(default_factory=list[RelatedAnime])
    recommendations: List[Recommendation] = field(default_factory=list[Recommendation])
    opening_themes: List[Song] = field(default_factory=list[Song])
    ending_themes: List[Song] = field(default_factory=list[Song])
    background: Optional[str] = None



