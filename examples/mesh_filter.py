import numpy as np
import open3d as o3d

from missing_kit.io import load_mesh


if __name__ == '__main__':
    points, colors, _ = load_mesh('./data/amiibo/amiibo_13.252699179954142.ply', load_all=True)
    # points, colors, _ = load_mesh('./data/egypt/egypt_6.470620605916311.ply', load_all=True)

    idx = np.invert(np.all(colors < 0.01, axis=1))
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[idx])
    pcd.colors = o3d.utility.Vector3dVector(colors[idx])
    o3d.visualization.draw([pcd], show_skybox=False, point_size=3, bg_color=(1.0, 1.0, 1.0, 1.0), show_ui=True)

    # save_mesh('./filtered.ply', points[idx], colors=colors[idx])
