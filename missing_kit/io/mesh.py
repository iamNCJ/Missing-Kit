import open3d as o3d
import numpy as np


def load_mesh(filename, load_all: bool = False):
    """
    Load mesh_process with Open3D
    :param filename: mesh_process file
    :param load_all: whether to load colors and normals
    :return:
        - points: `np.ndarray` (n, 3)
        - colors: `np.ndarray` (n, 3), will not be returned when `load_all` is set to False
        - normals: `np.ndarray` (n, 3), will not be returned when `load_all` is set to False
    """
    if load_all:
        data = o3d.io.read_point_cloud(filename)
        points = np.asarray(data.points)
        colors = np.asarray(data.colors)
        normals = np.asarray(data.normals)
        return points, colors, normals
    else:
        return np.asarray(o3d.io.read_point_cloud(filename).points)


def save_mesh(filename, points: np.ndarray, colors: np.ndarray = None, normals: np.ndarray = None,
              use_float32: bool = True):
    """
    Save mesh_process to file with Open3D
    :param filename: mesh_process file
    :param points: `np.ndarray` (n, 3)
    :param colors: `np.ndarray` (n, 3), set None if colors not available
    :param normals: `np.ndarray` (n, 3), set None if normals not available
    :param use_float32: store float32 values (for compatibility with `PCL`)
    """
    pcd = o3d.t.geometry.PointCloud()
    dtype = o3d.core.float32 if use_float32 else o3d.core.float64
    pcd.point['positions'] = o3d.core.Tensor(points, dtype)
    if colors is not None:
        pcd.point['colors'] = o3d.core.Tensor(colors, dtype)
    if normals is not None:
        pcd.point['normals'] = o3d.core.Tensor(normals, dtype)

    o3d.t.io.write_point_cloud(filename, pcd)
