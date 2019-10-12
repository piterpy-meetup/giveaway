from hashlib import sha256
from typing import List, Iterable, Generator, Any, Iterator

from giveaway.core.constants import VALID_USERNAME, ENCODING
from giveaway.core.typing import RawUserName, UserName, HashedUserName, Line


def prepare_username(uname: RawUserName) -> UserName:
    _, sep, name = uname.lower().rpartition("@")
    return UserName(name)


def hash_username(item: UserName) -> HashedUserName:
    h = sha256(item.encode(ENCODING))
    return h.hexdigest()


def process_usernames(unames: List[RawUserName]) -> List[HashedUserName]:
    prepared: Iterable[UserName] = (prepare_username(uname) for uname in unames)
    hashed: Iterable[HashedUserName] = sorted(
        hash_username(uname) for uname in prepared
    )
    result: List[HashedUserName] = list(hashed)
    return result


def is_valid_username(line: Line) -> bool:
    return bool(VALID_USERNAME.fullmatch(line))


def filter_usernames(lines: Generator[str, Any, None]) -> Iterator[RawUserName]:
    return filter(is_valid_username, map(lambda l: l.rstrip(), lines))
