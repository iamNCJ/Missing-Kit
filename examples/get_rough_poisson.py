from missing_kit.io import create_colmap_database
from missing_kit.shell import colmap


def get_poisson_mesh(database_name, undistorted_image_path, camera_params):
    create_colmap_database(database_name)
    colmap.feature_extractor(database_name, undistorted_image_path, camera_params)
    colmap.exhaustive_matcher(database_name)


if __name__ == '__main__':
    BASE_PATH = '/workspace/data/bigbigbig/LIGHT_FIELD_freshmeat/1_19_5models/amiibo/test_new_script'
    DB_FILE = f'{BASE_PATH}/database.db'
    IMAGE_PATH = f'{BASE_PATH}/30views'
    CAMERA_PARAMS = '2373.046104729776,2375.5106693944517,668.8785376738697,550.609404815664,0.0,0.0,0.0,0.0'

    get_poisson_mesh(
        database_name=DB_FILE,
        undistorted_image_path=IMAGE_PATH,
        camera_params=CAMERA_PARAMS
    )
