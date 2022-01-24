from missing_kit.shell import sh


def feature_extractor(database_file: str, image_path: str, camera_params: str):
    """
    Wrapper of COLMAP Feature Extractor
    :param database_file:
    :param image_path:
    :param camera_params:
    :return:
    """
    stdout, stderr, exit_code = sh('colmap feature_extractor '
                                   f'--database_path {database_file} '
                                   f'--image_path {image_path} '
                                   '--ImageReader.camera_model OPENCV '
                                   '--ImageReader.single_camera 1 '
                                   f'--ImageReader.camera_params {camera_params}')

    print(stdout)
    print(stderr)
    if exit_code != 0:
        raise RuntimeError('COLMAP Feature Extractor run failed!')


def exhaustive_matcher(database_file: str):
    """
    Wrapper of COLMAP Exhaustive Matcher
    :param database_file:
    :return:
    """
    stdout, stderr, exit_code = sh('colmap feature_extractor '
                                   f'--database_path {database_file}')

    print(stdout)
    print(stderr)
    if exit_code != 0:
        raise RuntimeError('COLMAP Exhaustive Matcher run failed!')
