"""
core.py
"""

import argparse
from datetime import datetime
from hercules.attack import BruteForce


def banner(usernames, passwords, threads):
    print('Hercules v0.0.1 (c) 2022 by Anvbis\n'
          'https://github.com/anvbis/hercules\n')

    attempts = usernames * passwords
    print(f'hercules.py: info: starting attack at {datetime.now()}\n'
          f'hercules.py: info: using {usernames} usernames, {passwords} passwords'
          f'; {attempts} tries, ~{attempts//threads} tries per thread')


def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', metavar='request',
        type=argparse.FileType('rb'),
        help='the raw HTTP request to emulate',
        required=True)

    user_group = parser.add_mutually_exclusive_group(required=True)
    user_group.add_argument('-u', metavar='username',
        help='a single username to use in brute-force attack')
    user_group.add_argument('-U', metavar='file',
        type=argparse.FileType('r'),
        help='a list of usernames to use in brute-force attack')

    passw_group = parser.add_mutually_exclusive_group(required=True)
    passw_group.add_argument('-p', metavar='password',
        help='a single password to use in brute-force attack')
    passw_group.add_argument('-P', metavar='file',
        type=argparse.FileType('r', errors='replace'),
        help='a list of passwords to use in brute-force attack')

    parser.add_argument('-f', metavar='fail',
        type=str,
        help='the substring expected in unsuccessful attempt',
        required=True)
    parser.add_argument('-t', metavar='threads',
        type=int,
        help='the number of concurrent threads (default: 20)',
        default=20)
    parser.add_argument('-k',
        help='force all connections to use TLS encryption',
        action='store_true')

    return parser.parse_args()


def main():
    args = arguments()
    raw_data = args.r.read()

    if args.U:
        usernames = [line.strip() for line in args.U.readlines()]
    else:
        usernames = [args.u]

    if args.P:
        passwords = [line.strip() for line in args.P.readlines()]
    else:
        passwords = [args.p]

    banner(len(usernames), len(passwords), args.t)

    brute_force = BruteForce(raw_data, args.t, args.f, args.k)
    brute_force.attack(usernames, passwords) 

