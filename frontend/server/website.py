from flask import render_template, redirect, url_for, request, session
from time import time
from os import urandom


class Website:
    def __init__(self, bp, url_prefix) -> None:
        self.bp = bp
        self.url_prefix = url_prefix
        self.routes = {
            '/': {
                'function': lambda: redirect(url_for('._index')),
                'methods': ['GET', 'POST']
            },
            '/chat/': {
                'function': self._index,
                'methods': ['GET', 'POST']
            },
            '/chat/<conversation_id>': {
                'function': self._chat,
                'methods': ['GET', 'POST']
            }
        }

    def _chat(self, conversation_id):
        if '-' not in conversation_id:
            return redirect(url_for('._index'))

        return render_template('index.html', chat_id=conversation_id, url_prefix=self.url_prefix)

    def _index(self):
        return render_template('index.html', chat_id=f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}', url_prefix=self.url_prefix)
