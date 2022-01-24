from missing_kit.shell import sh, mkdir


def feature_extractor(database_file: str, image_path: str, camera_params: str):
    """
    Wrapper of COLMAP Feature Extractor
    :param database_file:
    :param image_path:
    :param camera_params:
    """
    stdout, stderr, exit_code = sh('colmap feature_extractor '
                                   f'--database_path {database_file} '
                                   f'--image_path {image_path} '
                                   '--ImageReader.camera_model OPENCV '
                                   '--ImageReader.single_camera 1 '
                                   f'--ImageReader.camera_params {camera_params}')

    if exit_code != 0:
        print(stdout)
        print(stderr)
        raise RuntimeError('COLMAP Feature Extractor run failed!')


def exhaustive_matcher(database_file: str):
    """
    Wrapper of COLMAP Exhaustive Matcher
    :param database_file:
    """
    stdout, stderr, exit_code = sh('colmap exhaustive_matcher '
                                   f'--database_path {database_file} '
                                   '--SiftMatching.multiple_models 0 '
                                   '--SiftMatching.guided_matching 1')

    if exit_code != 0:
        print(stdout)
        print(stderr)
        raise RuntimeError('COLMAP Exhaustive Matcher run failed!')


def reconstruction_mapper(database_file, image_path, output_path):
    """
    Wrapper of COLMAP Mapper
    :param database_file:
    :param image_path:
    :param output_path:
    """
    mkdir(output_path)
    stdout, stderr, exit_code = sh('colmap mapper '
                                   f'--database_path {database_file} '
                                   f'--image_path {image_path} '
                                   f'--output_path {output_path} '
                                   '--Mapper.multiple_models 0 '
                                   '--Mapper.tri_ignore_two_view_tracks 0 '
                                   '--Mapper.ba_refine_focal_length 0 '
                                   '--Mapper.ba_refine_principal_point 0 '
                                   '--Mapper.ba_refine_extra_params 0 '
                                   '--Mapper.ba_global_use_pba 0')

    if exit_code != 0:
        print(stdout)
        print(stderr)
        raise RuntimeError('COLMAP Mapper run failed!')


def bundle_adjustment():
    pass
