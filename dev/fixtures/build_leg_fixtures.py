"""Build the synthetic mock-io fixtures for the `leg-names` test case.

Trimmed copy of patrol-effort-table's dev/fixtures/build_leg_fixtures.py (same
seed, same rows), keeping only the five frames this workflow's mock run reads.
The data MODEL is the mep-dev sample pulled on 2026-10-22 (never committed): the
column set, dtypes and nesting of the patrols / observations / legs frames an
EarthRanger site with the `patrol_schemas` flag returns. Every ROW here is made
up: uuid5 ids, invented ranger / team / vehicle names, a jittered straight-line
track. Only the patrol-type slug (`ecoscope_leg_test`, org config) is real.

Planted shape (what the test case asserts):
- 2 patrols, 3 legs: 08-12 and 13-16 on 2026-01-05 (patrol 1001), 09-11 on
  2026-01-06 (patrol 1002); every leg has the same team, 2 members and 1 asset.
- one fix every 10 minutes per leg (25 + 19 + 13 = 57), each leg walking east
  along lat -1.4.

Legs are derived from the nested `patrol_segments` with the library's own
`patrol_segments_from_patrols_df`, so the leg schema is the library's, not this
script's. The two name frames are what `add_patrol_team_names` and
`add_patrol_roster_names` return for those legs.

Run from the inner workflow env (after the editable compile):
    cd ecoscope-workflows-download-patrols-workflow
    pixi run --frozen python ../dev/fixtures/build_leg_fixtures.py
"""

import json
import uuid
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point

from ecoscope.io.earthranger_utils import patrol_segments_from_patrols_df

LEGS_DIR = Path(__file__).resolve().parent / "legs"
RNG = np.random.default_rng(20261022)


def fake_id(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"patrol-effort-table-fixture/{name}"))


SLUG, DISPLAY = "ecoscope_leg_test", "Ecoscope Leg Test"
TYPE_ID = fake_id("patrol-type/ecoscope_leg_test")
TEAM = ("Leg Test Team", fake_id("team/leg-test"))
MEMBERS = [("Ranger Amani", fake_id("subject/amani")), ("Ranger Baraka", fake_id("subject/baraka"))]
ASSET = ("Patrol Vehicle 1", fake_id("subject/vehicle-1"))
LEADER = MEMBERS[0]
SOURCE_ID = fake_id("source/amani-radio")
CREATED = "2026-01-02T08:00:00.000000Z"

# (serial, [(start, end), ...]) — one patrol per day, legs in UTC
PATROLS = [
    (1001, [("2026-01-05T08:00:00Z", "2026-01-05T12:00:00Z"), ("2026-01-05T13:00:00Z", "2026-01-05T16:00:00Z")]),
    (1002, [("2026-01-06T09:00:00Z", "2026-01-06T11:00:00Z")]),
]
LAT0, LON_START, LON_STEP, LEG_LON_OFFSET = -1.40, 36.90, 0.0045, 0.04
FIX_MINUTES = 10


def leader_dict() -> dict:
    return {
        "content_type": "observations.subject",
        "id": LEADER[1],
        "name": LEADER[0],
        "subject_type": "person",
        "subject_subtype": "ranger",
        "common_name": None,
        "additional": None,
        "created_at": CREATED,
        "updated_at": CREATED,
        "is_active": True,
        "user": None,
        "tracks_available": False,
        "image_url": "/static/ranger-black.svg",
    }


def build_patrols() -> pd.DataFrame:
    rows = []
    for serial, legs in PATROLS:
        patrol_id = fake_id(f"patrol/{serial}")
        segments = []
        for k, (start, end) in enumerate(legs):
            segments.append(
                {
                    "id": fake_id(f"segment/{serial}/{k}"),
                    "patrol_type": SLUG,
                    "leader": leader_dict(),
                    "scheduled_start": None,
                    "scheduled_end": None,
                    "time_range": {"start_time": start, "end_time": end},
                    "start_location": None,
                    "end_location": None,
                    "events": [],
                    "team": TEAM[1],
                    "members": [m[1] for m in MEMBERS],
                    "assets": [ASSET[1]],
                    "segment_details": {"weather": "dry"},
                    "type_details": None,
                    "is_pause": False,
                    "image_url": "https://example.invalid/static/sprite-src/generic_rep.svg",
                    "icon_id": "generic_rep",
                    "updates": [],
                }
            )
        rows.append(
            {
                "id": patrol_id,
                "priority": 0,
                "state": "done",
                "objective": None,
                "serial_number": serial,
                "title": f"Leg test patrol {serial}",
                "files": [],
                "notes": [],
                "patrol_segments": segments,
                "updates": [],
            }
        )
    return pd.DataFrame(rows)


def build_observations(patrols: pd.DataFrame) -> gpd.GeoDataFrame:
    frames = []
    leg_no = 0
    for _, patrol in patrols.iterrows():
        p_start = min(s["time_range"]["start_time"] for s in patrol["patrol_segments"])
        p_end = max(s["time_range"]["end_time"] for s in patrol["patrol_segments"])
        for seg in patrol["patrol_segments"]:
            times = pd.date_range(seg["time_range"]["start_time"], seg["time_range"]["end_time"], freq=f"{FIX_MINUTES}min", tz="UTC")
            n = len(times)
            lons = LON_START + leg_no * LEG_LON_OFFSET + LON_STEP * np.arange(n)
            lats = LAT0 + RNG.normal(0, 0.0004, size=n)
            frames.append(
                gpd.GeoDataFrame(
                    {
                        "extra__id": [fake_id(f"obs/{seg['id']}/{i}") for i in range(n)],
                        "extra__location": [{"latitude": float(y), "longitude": float(x)} for x, y in zip(lons, lats)],
                        "extra__created_at": pd.Timestamp(CREATED, tz="UTC"),
                        "extra__recorded_at": times,
                        "extra__source": SOURCE_ID,
                        "extra__exclusion_flags": 0,
                        "extra__subject_id": LEADER[1],
                        "groupby_col": patrol["id"],
                        "fixtime": times,
                        "junk_status": False,
                        "patrol_id": patrol["id"],
                        "patrol_title": patrol["title"],
                        "patrol_serial_number": int(patrol["serial_number"]),
                        "patrol_start_time": pd.Timestamp(p_start, tz="UTC"),
                        "patrol_end_time": pd.Timestamp(p_end, tz="UTC"),
                        "patrol_type": TYPE_ID,
                        "patrol_status": "done",
                        "patrol_subject": LEADER[0],
                        "patrol_segment_id": seg["id"],
                        "patrol_team": seg["team"],
                        "patrol_members": [list(seg["members"])] * n,
                        "patrol_assets": [list(seg["assets"])] * n,
                        "patrol_segment_details": json.dumps(seg["segment_details"]),
                        "patrol_type_details": json.dumps({}),
                        "patrol_type__value": SLUG,
                        "patrol_type__display": DISPLAY,
                        "patrol_type__icon": "",
                    },
                    geometry=[Point(x, y) for x, y in zip(lons, lats)],
                    crs=4326,
                )
            )
            leg_no += 1
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=4326)


def name_chain(legs: pd.DataFrame, team_names: dict, subject_names: dict) -> dict[str, pd.DataFrame]:
    """The two io name tasks' returns, each = its input + the columns it adds (mock chains)."""
    team = legs.copy()
    team["patrol_team_name"] = team["patrol_team"].map(lambda t: "None" if pd.isna(t) else team_names.get(t, t))
    roster = team.copy()
    for src, dst in {"patrol_members": "patrol_member_names", "patrol_assets": "patrol_asset_names"}.items():
        roster[dst] = roster[src].map(lambda ids: [subject_names.get(i, i) for i in list(ids)])
    return {"legs-team-names": team, "legs-roster-names": roster}


def write(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def main() -> None:
    patrols = build_patrols()
    obs = build_observations(patrols)
    legs = patrol_segments_from_patrols_df(patrols)
    names = name_chain(legs, team_names={TEAM[1]: TEAM[0]}, subject_names={i: n for n, i in MEMBERS + [ASSET]})

    write(patrols, LEGS_DIR / "patrols.parquet")
    write(obs, LEGS_DIR / "observations.parquet")
    write(legs, LEGS_DIR / "legs.parquet")
    for stem, frame in names.items():
        write(frame, LEGS_DIR / f"{stem}.parquet")
    print(f"patrols {len(patrols)}, observations {len(obs)}, legs {len(legs)}")


if __name__ == "__main__":
    main()
