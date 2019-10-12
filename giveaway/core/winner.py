from datetime import datetime, timezone
from hashlib import sha256
from random import seed, choice
from typing import List, Optional

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


def choose_winner(
    hashed_participants: List[HashedUserName], date: datetime
) -> HashedUserName:
    """
    Chooses a winner from a provided list of participants. Note, that to find out the real username we need to call a
    find_winner after all.

    :return: winner's hashed username
    """
    seed(count_seed(hashed_participants, date))
    return choice(hashed_participants)


def verify_winner(uname: UserName, hashed_uname: HashedUserName) -> bool:
    calculated = hash_username(uname)
    return calculated == hashed_uname


def find_winner(
    hashed_uname: HashedUserName, participants: List[UserName]
) -> Optional[UserName]:
    """
    Given a hashed username and a list of participants' usernames returns a winners' username.
    """
    for participant in participants:
        if verify_winner(participant, hashed_uname):
            return participant
