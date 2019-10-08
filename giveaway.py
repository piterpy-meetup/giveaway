import re
from datetime import datetime, timezone
from hashlib import sha256
from random import choice, seed
from typing import List, Iterable, Optional, NewType, Generator, Any, Iterator

ENCODING = 'utf-8'
VALID_USERNAME = re.compile(r'^@?[0-9A-Za-z_]+$')

Line = NewType('Line', str)
RawUserName = NewType('RawUserName', str)
UserName = NewType('UserName', str)
HashedUserName = NewType('HashedUserName', str)
Seed = NewType('Seed', str)


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
    binary_ts = int(ts).to_bytes(32, 'big')
    h.update(binary_ts)
    return h.hexdigest()


def choose_winner(hashed_participants: List[HashedUserName], date: datetime) -> HashedUserName:
    """
    Chooses a winner from a provided list of participants. Note, that to find out the real username we need to call a
    find_winner after all.

    :return: winner's hashed username
    """
    seed(count_seed(hashed_participants, date))
    return choice(hashed_participants)


def prepare_username(uname: RawUserName) -> UserName:
    _, sep, name = uname.lower().rpartition('@')
    return UserName(name)


def hash_username(item: UserName) -> HashedUserName:
    h = sha256(item.encode(ENCODING))
    return h.hexdigest()


def process_usernames(unames: List[RawUserName]) -> List[HashedUserName]:
    prepared: Iterable[UserName] = (prepare_username(uname) for uname in unames)
    hashed: Iterable[HashedUserName] = sorted(hash_username(uname) for uname in prepared)
    result: List[HashedUserName] = list(hashed)
    return result


def verify_winner(uname: UserName, hashed_uname: HashedUserName) -> bool:
    calculated = hash_username(uname)
    return calculated == hashed_uname


def find_winner(hashed_uname: HashedUserName, participants: List[UserName]) -> Optional[UserName]:
    """
    Given a hashed username and a list of participants' usernames returns a winners' username.
    """
    for participant in participants:
        if verify_winner(participant, hashed_uname):
            return participant


def is_valid(line: Line) -> bool:
    return bool(VALID_USERNAME.fullmatch(line))


def filter_usernames(lines: Generator[str, Any, None]) -> Iterator[RawUserName]:
    return filter(is_valid, map(lambda l: l.rstrip(), lines))
