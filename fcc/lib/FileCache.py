import hashlib
import os
import pickle


class FileCache:

    # Needs to be set by "someone else"
    cache_path = ''


    @classmethod
    def get(cls, key):
        h = hashlib.sha1( key.encode() )
        hash = h.hexdigest()
        path = f'{cls.cache_path}/{hash}.pickle'

        data = None
        if os.path.isfile(path):
            with open(path, 'rb') as fp:
                data = pickle.load(fp)

        return data


    @classmethod
    def put(cls, key, data):
        if not os.path.isdir(cls.cache_path):
            os.mkdir(cls.cache_path, 0o755)

        h = hashlib.sha1( key.encode() )
        hash = h.hexdigest()
        path = f'{cls.cache_path}/{hash}.pickle'

        with open(path, 'wb') as fp:
            pickle.dump(data, fp)
