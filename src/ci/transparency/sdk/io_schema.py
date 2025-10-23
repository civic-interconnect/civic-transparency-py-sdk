"""sdk/io_schema.py.

JSON serialization for WindowAgg and related types.
"""

from datetime import datetime
from typing import Any, TypedDict

import orjson

from .digests import Digests, MinHashSig, SimHash64
from .hash_core import ContentHash
from .ids import HashId
from .window_agg import TopHash, WindowAgg


def _dt_to_iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


def _iso_to_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.rstrip("Z"))


class TopHashJson(TypedDict):
    """JSON-serializable representation of a TopHash entry."""

    hash: str
    count: int


class SimHash64Json(TypedDict):
    """JSON-serializable representation of a SimHash64 signature."""

    bits: str


class MinHashJson(TypedDict):
    """JSON-serializable representation of a MinHash signature."""

    k: int
    sig: list[str]


class DigestsJson(TypedDict, total=False):
    """JSON-serializable representation of Digests, possibly containing SimHash64 and/or MinHash signatures."""

    simhash64: SimHash64Json
    minhash: MinHashJson


class WindowAggJson(TypedDict, total=False):
    """JSON-serializable representation of a WindowAgg entry."""

    world_id: str
    topic_id: str
    window_start: str
    window_end: str
    n_messages: int
    n_unique_hashes: int
    dup_rate: float
    top_hashes: list[TopHashJson]
    hash_concentration: float
    burst_score: float
    type_mix: dict[str, int]
    time_histogram: list[int]
    digests: DigestsJson


def windowagg_to_json(agg: WindowAgg) -> WindowAggJson:
    """Convert a WindowAgg object to its JSON-serializable dictionary representation."""
    """Convert a WindowAgg object to its JSON-serializable dictionary representation.

    Args:
        agg (WindowAgg): The WindowAgg instance to serialize.

    Returns:
        WindowAggJson: A dictionary suitable for JSON serialization.
    """
    payload: WindowAggJson = {
        "world_id": agg.world_id,
        "topic_id": agg.topic_id,
        "window_start": _dt_to_iso(agg.window_start),
        "window_end": _dt_to_iso(agg.window_end),
        "n_messages": agg.n_messages,
        "n_unique_hashes": agg.n_unique_hashes,
        "dup_rate": agg.dup_rate,
        "top_hashes": [{"hash": str(th.hash.id), "count": th.count} for th in agg.top_hashes],
        "hash_concentration": agg.hash_concentration,
        "burst_score": agg.burst_score,
        "type_mix": {k: int(v) for k, v in agg.type_mix.items()},
        "time_histogram": list(agg.time_histogram),
    }
    if agg.digests:
        d: DigestsJson = {}
        if agg.digests.simhash64:
            d["simhash64"] = {"bits": hex(agg.digests.simhash64.bits)}
        if agg.digests.minhash:
            d["minhash"] = {
                "k": agg.digests.minhash.k,
                "sig": [hex(x) for x in agg.digests.minhash.sig],
            }
        payload["digests"] = d
    return payload


def windowagg_from_json(d: dict[str, Any]) -> WindowAgg:
    """Deserialize a dictionary into a WindowAgg object.

    Args:
        d (dict[str, Any]): The dictionary to deserialize.

    Returns:
        WindowAgg: The resulting WindowAgg object.
    """
    top: list[TopHash] = []
    for th in d.get("top_hashes", []):
        algo, value = th["hash"].split(":", 1)
        top.append(TopHash(ContentHash(HashId(algo, value)), int(th["count"])))
    dig = None
    if "digests" in d:
        dj = d["digests"]
        sh = SimHash64(int(dj["simhash64"]["bits"], 16)) if "simhash64" in dj else None
        mh = None
        if "minhash" in dj:
            mh = MinHashSig(
                k=int(dj["minhash"]["k"]),
                sig=tuple(int(x, 16) for x in dj["minhash"].get("sig", [])),
            )
        dig = Digests(simhash64=sh, minhash=mh)
    return WindowAgg(
        world_id=d["world_id"],
        topic_id=d["topic_id"],
        window_start=_iso_to_dt(d["window_start"]),
        window_end=_iso_to_dt(d["window_end"]),
        n_messages=int(d["n_messages"]),
        n_unique_hashes=int(d["n_unique_hashes"]),
        dup_rate=float(d["dup_rate"]),
        top_hashes=top,
        hash_concentration=float(d["hash_concentration"]),
        burst_score=float(d["burst_score"]),
        type_mix=d["type_mix"],
        time_histogram=d["time_histogram"],
        digests=dig,
    )


def dumps(obj: dict[str, Any]) -> bytes:
    """Serialize a dictionary object to a JSON-formatted bytes object using orjson.

    Args:
        obj (dict[str, Any]): The dictionary to serialize.

    Returns:
        bytes: The JSON-formatted bytes representation of the object.
    """
    return orjson.dumps(obj)


def loads(b: bytes) -> dict[str, Any]:
    """Deserialize a JSON-formatted bytes object to a dictionary using orjson.

    Args:
        b (bytes): The JSON-formatted bytes object to deserialize.

    Returns:
        dict[str, Any]: The resulting dictionary.
    """
    return orjson.loads(b)
