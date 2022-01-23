import numpy as np
import pymeshlab


def simplify_mesh(points: np.ndarray, sample_num: int = 1000):
    """
    Simplify mesh_process with meshlab
    :param points: `np.ndarray` (n, 3)
    :param sample_num: number of points to leave after simplification
    :return: `np.ndarray` (n, 3)
    """
    m = pymeshlab.Mesh(points)
    ms = pymeshlab.MeshSet()
    ms.add_mesh(m, "simplified_mesh")
    ms.point_cloud_simplification(
        samplenum=sample_num,
        radius=pymeshlab.Percentage(0),
        bestsampleflag=True,
        bestsamplepool=10,
        exactnumflag=False
    )
    m = ms.current_mesh()
    return np.asarray(m.vertex_matrix())
