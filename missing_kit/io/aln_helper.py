import numpy as np


def load_trans(filename):
    """
    Read alignment file and return transform matrices
    :param filename: `aln` file
    :return: `np.ndarray` transform matrix (4, 4)
    """
    with open(filename, 'r') as f:
        res = f.readlines()
        trans_1 = np.fromstring(''.join(res[3:7]), dtype=np.float32, sep=' ').reshape((4, 4))
        trans_2 = np.fromstring(''.join(res[9:13]), dtype=np.float32, sep=' ').reshape((4, 4))

    return trans_1, trans_2
