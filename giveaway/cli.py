from json import dump, load

import click

from giveaway.core.typing import UserName
from giveaway.core.usernames import (
    filter_usernames,
    prepare_username,
    process_usernames,
)
from giveaway.core.winner import (
    choose_winner,
    find_winner,
    verify_winner,
    hash_username,
)


@click.group()
def cli():
    """
    Program to choose a winner from a given list of participants. The seed used by PRNG depends only on a list of
    participants and a date provided. So for every set of parameters the giveaway results can be reproduced.
    """
    pass


@cli.command("prepare")
@click.argument("source", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("destination", type=click.Path(file_okay=True, dir_okay=False))
def prepare_original_cli(source, destination):
    """Parse a file with a of participants, clean it up and save to json"""
    with open(source) as fp:
        lines = (line for line in fp)
        valid_lines = filter_usernames(lines)
        prepared_usernames = [prepare_username(uname) for uname in valid_lines]

    with open(destination, "w") as ofp:
        dump(prepared_usernames, ofp)


@cli.command("choose")
@click.argument(
    "participants", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.argument("date", type=click.DateTime(formats=["%d-%m-%Y"]))
def choose_winner_cli(participants, date):
    """choose a winner from PARTICIPANTS while using DATE to count seed"""
    with open(participants) as fp:
        raw_usernames = load(fp)
    hashed_participants = process_usernames(raw_usernames)
    hashed_winner = choose_winner(hashed_participants, date)
    participants = [prepare_username(uname) for uname in raw_usernames]
    winner = find_winner(hashed_winner, participants)
    click.echo(winner)


@cli.command("prepare_hashed")
@click.argument("source", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("destination", type=click.Path(file_okay=True, dir_okay=False))
def prepare_hashed_cli(source, destination):
    """Hash a list of participants from SOURCE and save to DESTINATION"""
    with open(source) as fp:
        raw_usernames = load(fp)
        hashed_participants = process_usernames(raw_usernames)

    with open(destination, "w") as ofp:
        dump(hashed_participants, ofp)


@cli.command("verify_choice")
@click.argument(
    "hashed_participants", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.argument("date", type=click.DateTime(formats=["%d-%m-%Y"]))
@click.option(
    "--username", default=None, help="username to compare with a winner's hash"
)
def verify_choice_cli(hashed_participants, date, username):
    """
    Verify choice using a HASHED_PARTICIPANTS file and DATE. Optionally you can provide a username to verify
    that it was chosen.
    """
    with open(hashed_participants) as fp:
        hashed_participants = load(fp)
    hashed_winner = choose_winner(hashed_participants, date)
    click.echo(f"Winner's hash is {hashed_winner}.")
    if username:
        prepared_username = prepare_username(username)
        is_winner = verify_winner(prepared_username, hashed_winner)
        if is_winner:
            click.echo(f"Yup! {username} is definitely a winner.")
        else:
            click.echo(
                f"Unfortunately, {username} is not a winner. But don't worry, better luck next time!"
            )


@cli.command("verify_participant")
@click.argument(
    "hashed_participants", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.argument("username", type=UserName)
def verify_choice_cli(hashed_participants, username):
    """
    Verify given USERNAME is present in a HASHED_PARTICIPANTS file.
    """
    with open(hashed_participants) as fp:
        hashed_participants = load(fp)
    hashed_username = hash_username(prepare_username(username))
    click.echo(f"Hashed username: {hashed_username}")
    is_in_participants = hashed_username in hashed_participants
    if is_in_participants:
        click.echo(
            f"{username} may not be a winner. But it is present in a list of participants."
        )
    else:
        click.echo(f"{username} is a creep and does not belong here :(")
