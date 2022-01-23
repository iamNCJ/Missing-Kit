import numpy as np


def project(point_3d, focal, principal_point) -> np.ndarray:
    """
    Project points to camera plane
    :param point_3d: `np.ndarray` (n, 3)
    :param focal: `np.ndarray` (2, )
    :param principal_point: `np.ndarray` (2, )
    :return: point locations in camera plane, `np.ndarray` (n, 2)
    """
    point_2d = point_3d[:, 0:2]
    depth = point_3d[:, 2].reshape((-1, 1))
    # check no depth is behind camera plane
    assert np.min(depth) > 0

    # Do projection
    point_2d *= focal / depth
    point_2d += principal_point
    return point_2d


def soft_render(points, focal, principal_point, image_dimensions) -> np.ndarray:
    """
    Software renderer written with numpy
    - Note that it does not support depth test
    :param points: `np.ndarray` (n, 3)
    :param focal: `np.ndarray` (2, )
    :param principal_point: `np.ndarray` (2, )
    :param image_dimensions: `np.ndarray` (2, ) [h, w]
    :return: rendered image `np.ndarray` (h, w, 3)
    """
    # Create canvas
    h, w = image_dimensions.astype(int)
    image = np.zeros((h, w, 3))

    # Project to camera plane
    projected_points = project(points, focal, principal_point).astype(int)
    valid_mask = np.all([projected_points[:, 1] < h, projected_points[:, 0] < w], axis=0)

    # Draw to canvas
    projected_points = projected_points[valid_mask]
    image[projected_points[:, 1], projected_points[:, 0]] = 1.
    return image
