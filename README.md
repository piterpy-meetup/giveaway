# Giveaway

## General info

Giveaway is a simple command-line tool to pick a winner from a list of participants. It is written using deterministic
algorithm in order for results being reproducible for every set of parameters. Requires Python 3.6 and higher.

## Usage

Preparing a list of participants:
```bash
python -m giveaway prepare SOURCE DESTINATION
```
The command generates a json list of participants in destination from a provided source (file of newline-separated list
 of usernames). By a convention it is recommended to name a destination file by the date of the event 
 (i.e. 26-09-2019.json).
 
Choosing a winner:
```bash
python -m giveaway choose /path/to/26-09-2019.json
```
It prints out the username of the winner chosen from the list of the participants prepared on the 
previous step. Optionally you can provide a desired number of winners to choose. This could be done
 like that:
```bash
python -m giveaway choose /path/to/26-09-2019.json --n 2
```

You can also provide the date to be used as a part of seed explicitly:
```bash
python -m giveaway choose PARTICIPANTS 26-09-2019
```

Preparing a list of hashed participants:
```bash
python -m giveaway prepare_hashed /path/to/26-09-2019.json /path/to/hashed/26-09-2019.json
```

Verifying a given username is in the hashed list of participants:
```hash
python -m giveaway verify_participant /path/to/hashed/26-09-2019.json ave2me
```

Verifying a given username is a winner:
```hash
python -m giveaway verify_choice /path/to/hashed/26-09-2019.json --username ave2me
```

Getting help on available commands:
```bash
python -m giveaway --help
```

## Seed generation algorithm description

A general approach to get repeatable results using pseudorandom number generator is using seed. 

This is how the seed is generated in our case:

* Prepare a list of participant consisting of usernames in lowercase (without a @)
* Sort a list of participants in alphabetical order
* Hash every user name from a list using SHA-256
* Convert a event date to timestamp 
* Calculate hash from a list of hashed participants and use event timestamp as salt
* Derived value is used as seed for PRNG
