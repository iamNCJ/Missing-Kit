import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
from tqdm import tqdm
import open3d as o3d

from missing_kit.io import read_colmap_model, load_mesh, load_trans
from missing_kit.math.transform import matrix_from_r_t, apply_matrix, matrix_rotate_axis_angle
from missing_kit.math.fitting import fit_cylinder
from missing_kit.mesh_process import simplify_mesh, transform_mesh
from missing_kit.render import soft_render

if __name__ == '__main__':
    OBJECT_NAME = 'egypt_cat'
    BASE_PATH = f'/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/1_24_main_results/{OBJECT_NAME}'
    GROUNDTRUTH_FILE_PATH = f'/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/gts/{OBJECT_NAME}.ply'
    CAM_PARAMS = [2373.046104729776, 2375.5106693944517, 668.8785376738697, 550.609404815664]
    W, H = 1332, 1152

    DB_NAME = 'database.db'
    FULLON_IMAGE_PATH = f'{BASE_PATH}/fullon'
    AUTO_MASK_BASE_PATH = f'{BASE_PATH}/auto_mask'
    PICKED_IMAGE_PATH = f'{AUTO_MASK_BASE_PATH}/selected_views'
    OBJECT_FILE_PATH = f'{AUTO_MASK_BASE_PATH}/object.ply'
    TURNTABLE_FILE_PATH = f'{AUTO_MASK_BASE_PATH}/turntable.ply'
    ALN_FILE_PATH = f'{AUTO_MASK_BASE_PATH}/alignment.aln'
    SPARSE_MODEL = f'{AUTO_MASK_BASE_PATH}/sparse/0'

    cameras, images, points = read_colmap_model(SPARSE_MODEL)
    cam_poses = []
    M_cam_init = None
    for image in images.values():
        qw, qx, qy, qz = image.qvec
        r = R.from_quat([qx, qy, qz, qw])
        R_mat = r.as_matrix().reshape((3, 3))
        T_vec = image.tvec
        M_cam = matrix_from_r_t(R_mat, T_vec)
        if image.name == '0.png':
            M_cam_init = M_cam
        M_cam_inv = np.linalg.inv(M_cam)
        cam_pos = apply_matrix(M_cam_inv, np.zeros((1, 3)))
        cam_poses.append(cam_pos.T)

    turn_table_points = load_mesh(TURNTABLE_FILE_PATH)
    turn_table_points = simplify_mesh(turn_table_points, sample_num=10000)
    w_fit, C_fit, r_fit, fit_err = fit_cylinder(turn_table_points)

    cam_poses.append(C_fit)
    cam_poses.append(C_fit * r_fit + w_fit)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(cam_poses)
    o3d.io.write_point_cloud(f"{AUTO_MASK_BASE_PATH}/cam.ply", pcd)

    if np.dot(cam_poses[0].reshape((3,)) - C_fit, w_fit) > 0:
        w_fit *= -1

    # id_map = {}
    # with open('../data/images.json', 'r') as f:
    #     mapping = json.load(f)
    # for item in mapping:
    #     id_map[item['name']] = item['image_id']

    # with open('../data/new_images.txt', 'w') as f:
    #     for j in range(0, 360):
    #         M_Rotate_inv = np.linalg.inv(matrix_rotate_axis_angle(w_fit, C_fit, j * np.pi / 180.))
    #         M_cam_new = M_cam_init @ M_Rotate_inv
    #         M_cam_new_inv = np.linalg.inv(M_cam_new)
    #         cam_pos = apply_matrix(M_cam_new_inv, np.zeros((1, 3)))
    #         cam_poses.append(cam_pos.T)
    #         r = R.from_matrix(M_cam_new[0:3, 0:3])
    #         qx, qy, qz, qw = r.as_quat()
    #         tx, ty, tz = M_cam_new[0:3, 3]
    #         f.write(f'{id_map[f"{(360 - j) % 360}.png"]} {qw} {qx} {qy} {qz} {tx} {ty} {tz} 1 {(360 - j) % 360}.png\n\n')

    gt_points = load_mesh(GROUNDTRUTH_FILE_PATH)
    trans = load_trans(ALN_FILE_PATH)
    # gt_points = transform_mesh(gt_points, trans)
    # obj_points = load_mesh(OBJECT_FILE_PATH)
    # finetuned_trans = reg_rigid_3d(simplify_mesh(obj_points), simplify_mesh(gt_points))
    gt_points = transform_mesh(gt_points, trans)
    image_dimensions = np.array((H, W), dtype=np.float64)
    focal_lengths = np.array((CAM_PARAMS[0], CAM_PARAMS[1]), dtype=np.float64)
    principal_point = np.array((CAM_PARAMS[2], CAM_PARAMS[3]), dtype=np.float64)

    for i in tqdm(range(0, 360)):
        M_Rotate_inv = np.linalg.inv(matrix_rotate_axis_angle(w_fit, C_fit, i * np.pi / 180.))
        M_cam_new = M_cam_init @ M_Rotate_inv
        trans_points = apply_matrix(M_cam_new, gt_points)
        img = (soft_render(trans_points, focal_lengths, principal_point, image_dimensions) * 255).astype(np.uint8)
        img = cv2.dilate(img, kernel=np.ones((10, 10), 'uint8'))
        img = cv2.erode(img, kernel=np.ones((10, 10), 'uint8'))
        img = cv2.dilate(img, kernel=np.ones((10, 10), 'uint8'))
        cv2.imwrite(f'{BASE_PATH}/{i}/mask_obj_only2.png', img)
