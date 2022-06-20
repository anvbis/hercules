# Hercules

```
usage: hercules.py [-h] -r REQUEST [-u USERNAMES] [-p PASSWORDS] -f FAIL [-t THREADS] [-k]

options:
  -h, --help            show this help message and exit
  -r REQUEST, --request REQUEST
                        the raw HTTP(S) request to emulate
  -u USERNAMES, --usernames USERNAMES
                        a list of usernames to use in brute-force attack
  -p PASSWORDS, --passwords PASSWORDS
                        a list of passwords to use in brute-force attack
  -f FAIL, --fail FAIL  the substring expected in unsuccessful attempt
  -t THREADS, --threads THREADS
                        the number of concurrent threads (default: 40)
  -k, --tls             force connections to utilise HTTPS protocol
```

```
POST /login.php HTTP/1.1
Host: example.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
Origin: http://example.org
Connection: close
Referer: http://example.org/login.php
Cookie: PHPSESSID=48mdpq6or5cu5aije94v4vcf8d
Upgrade-Insecure-Requests: 1

username=^USER^&password=^PASS^
```

```
./hercules.py -r request.txt -u usernames.lst -p passwords.lst -f 'Invalid credentials'
```
