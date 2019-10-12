# Giveaway

## General info

Giveaway is a simple command-line tool to pick a winner from a list of participants. It is written using deterministic
algorithm in order for results being reproducible for every set of parameters. Requires Python 3.6 and higher.

## Usage

Basic usage:
```bash
python -m giveaway COMMAND
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
