from missing_kit.io import create_colmap_database
from missing_kit.shell import colmap


def get_poisson_mesh(database_name, undistorted_image_path, camera_params, sparse_model_path, dense_model_path):
    create_colmap_database(database_name)
    colmap.feature_extractor(database_name, undistorted_image_path, camera_params)
    colmap.exhaustive_matcher(database_name)
    colmap.reconstruction_mapper(database_name, undistorted_image_path, sparse_model_path)
    colmap.bundle_adjustment(f'{sparse_model_path}/0')
    colmap.image_undistortion(undistorted_image_path, f'{sparse_model_path}/0', dense_model_path)
    colmap.dense_model_stereo(dense_model_path)
    colmap.dense_model_fusion(dense_model_path, f'{dense_model_path}/fused.ply')
    colmap.poisson_mesher(f'{dense_model_path}/fused.ply', f'{dense_model_path}/meshed_poisson.ply')


if __name__ == '__main__':
    BASE_PATH = '/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/1_19_5models/amiibo/test_new_script'
    DB_FILE = f'{BASE_PATH}/database.db'
    IMAGE_PATH = f'{BASE_PATH}/30views'
    CAMERA_PARAMS = '2373.046104729776,2375.5106693944517,668.8785376738697,550.609404815664,0.0,0.0,0.0,0.0'
    SPARSE_MODEL_PATH = f'{BASE_PATH}/sparse'
    DENSE_MODEL_PATH = f'{BASE_PATH}/dense'

    get_poisson_mesh(
        database_name=DB_FILE,
        undistorted_image_path=IMAGE_PATH,
        camera_params=CAMERA_PARAMS,
        sparse_model_path=SPARSE_MODEL_PATH,
        dense_model_path=DENSE_MODEL_PATH
    )
