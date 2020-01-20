import os
import errno


def ensure_dir(directory):
    if not os.path.isdir(directory):
        mkdir_p(directory)
    return os.path.abspath(directory)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
