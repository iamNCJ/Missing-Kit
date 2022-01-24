from missing_kit.io import create_colmap_database
from missing_kit.shell import colmap


def get_poisson_mesh(base_path, database_name, image_path, camera_params, output_poisson):
    database_name = f'{base_path}/{database_name}'
    sparse_model_path = f'{base_path}/sparse'
    dense_model_path = f'{base_path}/dense'

    create_colmap_database(database_name)
    colmap.feature_extractor(database_name, image_path, camera_params)
    colmap.exhaustive_matcher(database_name)
    colmap.reconstruction_mapper(database_name, image_path, sparse_model_path)
    colmap.bundle_adjustment(f'{sparse_model_path}/0')
    colmap.image_undistortion(image_path, f'{sparse_model_path}/0', dense_model_path)
    colmap.dense_model_stereo(dense_model_path)
    colmap.dense_model_fusion(dense_model_path, f'{dense_model_path}/fused.ply')
    colmap.poisson_mesher(f'{dense_model_path}/fused.ply', output_poisson)


if __name__ == '__main__':
    BASE_PATH = '/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/1_19_5models/amiibo/test_new_script'
    DB_NAME = 'database.db'
    IMAGE_PATH = f'{BASE_PATH}/30views'
    CAMERA_PARAMS = '2373.046104729776,2375.5106693944517,668.8785376738697,550.609404815664,0.0,0.0,0.0,0.0'
    POISSON_FILE_PATH = f'{BASE_PATH}/mesh_poisson.ply'

    get_poisson_mesh(
        base_path=BASE_PATH,
        database_name=DB_NAME,
        image_path=IMAGE_PATH,
        camera_params=CAMERA_PARAMS,
        output_poisson=POISSON_FILE_PATH
    )
