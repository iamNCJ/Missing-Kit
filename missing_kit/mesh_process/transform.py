import numpy as np


def transform_mesh(points: np.ndarray, trans: np.ndarray):
    """
    Apply transform to the points in mesh_process
    :param points: `np.ndarray` (n, 3)
    :param trans: `np.ndarray` (4, 4)
    :return: `np.ndarray` (n, 3)
    """
    points = np.concatenate([points, np.ones([points.shape[0], 1], np.float32)], axis=1)
    return (trans @ points.T).T[:, :3]
