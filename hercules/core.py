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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--request',
        type=argparse.FileType('rb'),
        help='the raw HTTP(S) request to emulate',
        required=True)
    parser.add_argument('-u', '--usernames',
        type=argparse.FileType('r'),
        help='a list of usernames to use in brute-force attack',
        required=True)
    parser.add_argument('-p', '--passwords',
        type=argparse.FileType('r', errors='replace'),
        help='a list of passwords to use in brute-force attack',
        required=True)
    parser.add_argument('-f', '--fail',
        type=str,
        help='the substring expected in unsuccessful attempt',
        required=True)
    parser.add_argument('-t', '--threads',
        type=int,
        help='the number of concurrent threads (default: 20)',
        default=20)
    parser.add_argument('-k', '--tls',
        help='force connections to utilise HTTPS protocol',
        action='store_true')

    args = parser.parse_args()
    raw_data = args.request.read()
    brute_force = BruteForce(raw_data, args.threads, args.fail)
    
    usernames = [line.strip() for line in args.usernames.readlines()]
    passwords = [line.strip() for line in args.passwords.readlines()]

    banner(len(usernames), len(passwords), args.threads)
    brute_force.attack(usernames, passwords) 

