import json
import os
from pathlib import Path
from typing import Dict

import pandas as pd

from .path_finder import PathFinder


def read_index(path: str) -> Dict:
    """Reads the data index, removing the initial stages of nesting."""
    path = Path(path)
    kind = os.path.splitext(path.name)[0]
    data = json.loads(path.read_text())
    return data["protocols"][kind]["subjects"]


def _index_dict_to_dataframe(data: Dict) -> pd.DataFrame:
    subjects = data.keys()
    entries = []

    for subject in subjects:
        experiments = data[subject]["experiments"]
        for experiment in experiments:
            sessions = experiments[experiment]["sessions"]
            for session in sessions:
                entry = sessions[session]
                entry["subject"] = subject
                entry["experiment"] = experiment
                entry["session"] = int(session)
                entries.append(entry)

    df = pd.DataFrame(entries)
    return df


def get_data_index(kind: str = "all", rootdir: str = "/") -> pd.DataFrame:
    """Get an index to all available data.

    Parameters
    ----------
    kind
        Which kind of data index to return (default: "all"). Choices are:
        ``"r1"``, ``"ltp"``, ``"all"``. Using ``"all"`` will read all available
        indices.
    rootdir
        Root search path (default: ``"/"``).

    Returns
    -------
    index
        A flattened :class:`pd.DataFrame` version of the data index.

    """
    kinds = ("r1", "ltp", "all")

    if kind not in kinds:
        raise ValueError("Unknown data index: " + kind)

    finder = PathFinder(rootdir=rootdir)
    data = []

    if kind == "ltp" or kind == "all":
        data.append(read_index(finder.find("ltp_index")))
    if kind == "r1" or kind == "all":
        data.append(read_index(finder.find("r1_index")))

    df = pd.concat([_index_dict_to_dataframe(d) for d in data])
    return df