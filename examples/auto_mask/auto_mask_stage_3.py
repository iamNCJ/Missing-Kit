from missing_kit.io import create_colmap_database, get_images_from_colmap_db
from missing_kit.shell import colmap, mkdir

if __name__ == '__main__':
    OBJECT_NAME = 'egypt'
    BASE_PATH = f'/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/1_24_lambda_comp/{OBJECT_NAME}'
    CAMERA_PARAMS = '2373.046104729776,2375.5106693944517,668.8785376738697,550.609404815664,0.0,0.0,0.0,0.0'

    DB_NAME = 'database.db'
    NEW_IMAGE_PATH = f'{BASE_PATH}/test_mask'
    SFM_PATH = f'{BASE_PATH}/sfm_test'
    DB_PATH = f'{SFM_PATH}/{DB_NAME}'

    mkdir(SFM_PATH)
    create_colmap_database(DB_PATH)
    colmap.feature_extractor(DB_PATH, NEW_IMAGE_PATH, CAMERA_PARAMS)
    colmap.exhaustive_matcher(DB_PATH)

    images = get_images_from_colmap_db(DB_PATH)
    id_map = {}
    for image in images:
        print(image)

    # cameras, images, points = read_colmap_model(DENSE_MODEL)
    # cam_poses = []
    # M_cam_init = None
    # for image in images.values():
    #     qw, qx, qy, qz = image.qvec
    #     r = R.from_quat([qx, qy, qz, qw])
    #     R_mat = r.as_matrix().reshape((3, 3))
    #     T_vec = image.tvec
    #     M_cam = matrix_from_r_t(R_mat, T_vec)
    #     if image.name == '0.png':
    #         M_cam_init = M_cam
    #     M_cam_inv = np.linalg.inv(M_cam)
    #     cam_pos = apply_matrix(M_cam_inv, np.zeros((1, 3)))
    #     cam_poses.append(cam_pos.T)
    #
    # turn_table_points = load_mesh(TURNTABLE_FILE_PATH)
    # turn_table_points = simplify_mesh(turn_table_points, sample_num=10000)
    # w_fit, C_fit, r_fit, fit_err = fit_cylinder(turn_table_points)
    #
    # cam_poses.append(C_fit)
    # cam_poses.append(C_fit * r_fit + w_fit)
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(cam_poses)
    # o3d.io.write_point_cloud(f"{AUTO_MASK_BASE_PATH}/cam.ply", pcd)
    #
    # if np.dot(cam_poses[0].reshape((3,)) - C_fit, w_fit) > 0:
    #     w_fit *= -1
    #
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
