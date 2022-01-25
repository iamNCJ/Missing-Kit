import numpy as np


def matrix_origin_axis_and_angle(u, theta):
    """
    (4, 4)
    :param u:
    :param theta:
    :return:
    """
    x = u[0]
    y = u[1]
    z = u[2]
    s = np.sin(theta)
    c = np.cos(theta)

    return np.array([[c + x ** 2 * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s, 0],
                     [y * x * (1 - c) + z * s, c + y ** 2 * (1 - c), y * z * (1 - c) - x * s, 0],
                     [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z ** 2 * (1 - c), 0],
                     [0, 0, 0, 1]])


def matrix_translate(t):
    """
    (4, 4)
    :param t: (3, )
    :return:
    """
    res = np.eye(4)
    res[0:3, 3] = t
    return res


def matrix_from_r_t(r, t):
    """
    (4, 4)
    :param r:
    :param t:
    :return:
    """
    res = np.eye(4)
    res[0:3, 0:3] = r
    res[0:3, 3] = t
    return res


def apply_matrix(m, p):
    """
    (n, 3)
    :param m:
    :param p:
    :return: (n, 3)
    """
    p = np.concatenate([p, np.ones([p.shape[0], 1])], axis=1)
    return (m @ p.T).T[:, :3]


def matrix_rotate_axis_angle(w, c, angle):
    """
    (4, 4)
    :param w:
    :param c:
    :param angle:
    :return:
    """
    return (matrix_translate(c) @ matrix_origin_axis_and_angle(w, angle)) @ matrix_translate(-c)
