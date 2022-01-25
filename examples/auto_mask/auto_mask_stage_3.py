import numpy as np

from missing_kit.io import create_colmap_database, get_images_from_colmap_db, read_colmap_model, load_mesh
from missing_kit.numerics.transform import matrix_from_r_t, apply_matrix, matrix_rotate_axis_angle
from missing_kit.mesh_process import simplify_mesh
from missing_kit.shell import colmap, mkdir
from missing_kit.numerics.fitting import fit_cylinder
from scipy.spatial.transform import Rotation as R

if __name__ == '__main__':
    for OBJECT_NAME in ['conch', 'big_white', 'egypt']:
        BASE_PATH = f'/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/1_24_main_results/{OBJECT_NAME}'
        CAMERA_PARAMS = '2373.046104729776,2375.5106693944517,668.8785376738697,550.609404815664,0.0,0.0,0.0,0.0'

        DB_NAME = 'database.db'
        NEW_IMAGE_PATH = f'{BASE_PATH}/fullon'
        SFM_PATH = f'{BASE_PATH}/sfm'
        DB_PATH = f'{SFM_PATH}/{DB_NAME}'

        AUTO_MASK_BASE_PATH = f'{BASE_PATH}/auto_mask'
        SPARSE_MODEL = f'{AUTO_MASK_BASE_PATH}/sparse/0'

        mkdir(SFM_PATH)
        create_colmap_database(DB_PATH)
        colmap.feature_extractor(DB_PATH, NEW_IMAGE_PATH, CAMERA_PARAMS)
        colmap.exhaustive_matcher(DB_PATH)

        images = get_images_from_colmap_db(DB_PATH)
        id_map = {}
        for image in images:
            image_id = image[0]
            filename = image[1]
            id_map[filename] = image_id

        cameras, images, points = read_colmap_model(SPARSE_MODEL)
        image = images[1]
        qw, qx, qy, qz = image.qvec
        r = R.from_quat([qx, qy, qz, qw])
        R_mat = r.as_matrix().reshape((3, 3))
        T_vec = image.tvec
        M_cam = matrix_from_r_t(R_mat, T_vec)
        M_cam_inv = np.linalg.inv(M_cam)
        cam_pos = apply_matrix(M_cam_inv, np.zeros((1, 3)))

        TURNTABLE_FILE_PATH = f'{AUTO_MASK_BASE_PATH}/turntable.ply'
        turn_table_points = load_mesh(TURNTABLE_FILE_PATH)
        turn_table_points = simplify_mesh(turn_table_points, sample_num=10000)
        w_fit, C_fit, r_fit, fit_err = fit_cylinder(turn_table_points)

        if np.dot(cam_pos.reshape((3,)) - C_fit, w_fit) > 0:
            w_fit *= -1

        MANUAL_MODEL_PATH = f'{SFM_PATH}/manual'
        mkdir(MANUAL_MODEL_PATH)

        with open(f'{MANUAL_MODEL_PATH}/images.txt', 'w') as f:
            for j in range(0, 360):
                M_Rotate_inv = np.linalg.inv(matrix_rotate_axis_angle(w_fit, C_fit, j * np.pi / 180.))
                M_cam_new = M_cam @ M_Rotate_inv
                M_cam_new_inv = np.linalg.inv(M_cam_new)
                cam_pos = apply_matrix(M_cam_new_inv, np.zeros((1, 3)))
                r = R.from_matrix(M_cam_new[0:3, 0:3])
                qx, qy, qz, qw = r.as_quat()
                tx, ty, tz = M_cam_new[0:3, 3]
                f.write(f'{id_map[f"{j}.png"]} {qw} {qx} {qy} {qz} {tx} {ty} {tz} 1 {j}.png\n\n')

        with open(f'{MANUAL_MODEL_PATH}/cameras.txt', 'w') as f:
            f.write("""# Camera list with one line of data per camera:
    #   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
    # Number of cameras: 1
    1 OPENCV 1332 1152 2373.05 2375.51 668.879 550.609 0 0 0 0
    """)

        with open(f'{MANUAL_MODEL_PATH}/points3D.txt', 'w') as f:
            f.write('')

        mkdir(f'{SFM_PATH}/triangulate')
        colmap.point_triangulator(DB_PATH, NEW_IMAGE_PATH, f'{SFM_PATH}/manual', f'{SFM_PATH}/triangulate')
