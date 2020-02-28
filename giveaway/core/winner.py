import os
from datetime import datetime, timezone
from hashlib import sha256
from random import seed, choice
from typing import List

from giveaway.core.constants import ENCODING
from giveaway.core.typing import HashedUserName, Seed, UserName
from giveaway.core.usernames import hash_username


def count_seed(hashed_participants: List[HashedUserName], date: datetime) -> Seed:
    """
    The idea is to use seed to be able to reproduce giveaway results. In the current implementation we use seed that
    only depends on a list of participants' username hashes and the event date.

    :return: seed
    """
    h = sha256()
    for participant in hashed_participants:
        h.update(participant.encode(ENCODING))
    ts = date.replace(tzinfo=timezone.utc).timestamp()
    binary_ts = int(ts).to_bytes(32, "big")
    h.update(binary_ts)
    return h.hexdigest()


def choose_winners(
    hashed_participants: List[HashedUserName], date: datetime, n: int = 1
) -> List[HashedUserName]:
    """
    Chooses a winner from a provided list of participants. Note, that to find out the real username we need to call a
    find_winner after all.

    :return: winner's hashed username
    """
    seed(count_seed(hashed_participants, date))
    return [choice(hashed_participants) for _ in range(n)]


def verify_winner(uname: UserName, hashed_uname: HashedUserName) -> bool:
    calculated = hash_username(uname)
    return calculated == hashed_uname


def find_winners(
    hashed_unames: List[HashedUserName], participants: List[UserName]
) -> List[UserName]:
    """
    Given a hashed username and a list of participants' usernames returns a winners' username.
    """
    winners = []
    for participant in participants:
        if any(
            verify_winner(participant, hashed_uname) for hashed_uname in hashed_unames
        ):
            winners.append(participant)
    return winners


def get_date_from_filename(filename: str) -> datetime:
    filename = os.path.basename(filename)
    name, _extension = os.path.splitext(filename)
    return datetime.strptime(name, "%d-%m-%Y")
