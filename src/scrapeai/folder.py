from pathlib import Path

from itertools import chain

from .file import File


ALLOWED_FILE_SUFFIXES = ['.pdf', '.txt', '.tsv', '.csv', '.md', '*']


class Folder:

    def __init__(self, path=None, files_endwith=None, client=None):
        if path is None:
            raise ValueError('Must specify `path` to folder that contains files.')
        if files_endwith is None or not files_endwith:
            raise ValueError('Must specify `files_endwith` suffix.')
        for value in files_endwith:
            if value not in ALLOWED_FILE_SUFFIXES:
                raise ValueError(f'{value} invalid for `files_endwith`, must be one of {ALLOWED_FILE_SUFFIXES}.')
        if client is None:
            raise ValueError('Must specify API `client`.')
        self.path = path
        self.files_endwith = files_endwith
        self.client = client

    def get_files(self):
        return [
            File(f)
            for f in chain.from_iterable(
                    Path(self.path).glob(f'*{suffix}')
                    for suffix in self.files_endwith
            )
        ]

    @property
    def files(self):
        return [f.path.name for f in self.get_files()]

    def ask(self, question):
        pass
