from json import dump, load

import click

from giveaway import filter_usernames, prepare_username, process_usernames, choose_winner, find_winner


@click.group()
def cli():
    pass


@cli.command('prepare')
@click.argument('inputfile', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('outputfile', type=click.Path(file_okay=True, dir_okay=False))
def prepare_raw_cli(inputfile, outputfile):
    with open(inputfile) as fp:
        lines = (line for line in fp)
        valid_lines = filter_usernames(lines)
        prepared_usernames = [prepare_username(uname) for uname in valid_lines]

    with open(outputfile, 'w') as ofp:
        dump(prepared_usernames, ofp)


@cli.command('choose')
@click.argument('participants', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('date', type=click.DateTime(formats=['%d-%m-%Y']))
def choose_winner_cli(participants, date):
    with open(participants, 'r') as fp:
        raw_usernames = load(fp)
        participants = [prepare_username(uname) for uname in raw_usernames]
        hashed_participants = process_usernames(raw_usernames)
        hashed_winner = choose_winner(hashed_participants, date)
        winner = find_winner(hashed_winner, participants)
        click.echo(winner)


if __name__ == '__main__':
    cli()
