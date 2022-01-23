import open3d as o3d
import numpy as np

from missing_kit.render import visualize_mesh


# TODO: rewrite, redesign interface
if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud('./data/meshed-poisson.ply')
    # o3d.visualization.draw([pcd], show_skybox=False, point_size=3, bg_color=(1.0, 1.0, 1.0, 1.0), show_ui=True)
    visualize_mesh(pcd)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    assert points.shape == colors.shape
    data = np.hstack([points, colors])
    np.savetxt('./data/point_light_colmap.txt', data, fmt='%10.5f')
