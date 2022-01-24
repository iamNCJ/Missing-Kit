from missing_kit.shell import sh, mkdir


# TODO: finish docstrings
def feature_extractor(database_file: str, image_path: str, camera_params: str):
    """
    Wrapper of COLMAP Feature Extractor
    :param database_file:
    :param image_path:
    :param camera_params:
    """
    output, exit_code = sh('colmap feature_extractor '
                           f'--database_path {database_file} '
                           f'--image_path {image_path} '
                           '--ImageReader.camera_model OPENCV '
                           '--ImageReader.single_camera 1 '
                           f'--ImageReader.camera_params {camera_params}')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Feature Extractor run failed!')


def exhaustive_matcher(database_file: str):
    """
    Wrapper of COLMAP Exhaustive Matcher
    :param database_file:
    """
    output, exit_code = sh('colmap exhaustive_matcher '
                           f'--database_path {database_file} '
                           '--SiftMatching.multiple_models 0 '
                           '--SiftMatching.guided_matching 1')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Exhaustive Matcher run failed!')


def reconstruction_mapper(database_file, image_path, output_path):
    """
    Wrapper of COLMAP Mapper
    :param database_file:
    :param image_path:
    :param output_path:
    """
    mkdir(output_path)
    output, exit_code = sh('colmap mapper '
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
        print(output)
        raise RuntimeError('COLMAP Mapper run failed!')


def bundle_adjustment(model_path):
    """
    Wrapper of COLMAP Bundle Adjuster
    :param model_path:
    """
    output, exit_code = sh('colmap bundle_adjuster '
                           f'--input_path {model_path} '
                           f'--output_path {model_path} '
                           '--BundleAdjustment.refine_focal_length 0 '
                           '--BundleAdjustment.refine_principal_point 0 '
                           '--BundleAdjustment.refine_extra_params 0 '
                           '--BundleAdjustment.refine_extrinsics 1')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Bundle Adjuster run failed!')


def image_undistortion(image_path, model_path, output_path):
    """
    Wrapper of COLMAP Image Undistortor
    :param image_path:
    :param model_path:
    :param output_path:
    """
    # TODO: add roi
    output, exit_code = sh('colmap image_undistorter '
                           f'--input_path {model_path} '
                           f'--image_path {image_path} '
                           f'--output_path {output_path}')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Image Undistortor run failed!')


def dense_model_stereo(model_path):
    """
    Wrapper of COLMAP Dense 3D Stereo Reconstruction
    :param: model_path
    """
    output, exit_code = sh('colmap patch_match_stereo '
                           f'--workspace_path {model_path}')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Dense 3D Stereo run failed!')


def dense_model_fusion(model_path, output_path):
    """
    Wrapper of COLMAP Fusion
    :param: model_path
    """
    output, exit_code = sh('colmap stereo_fusion '
                           f'--workspace_path {model_path} '
                           f'--output_path {output_path}')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Fusion run failed!')


def poisson_mesher(input_file, output_file, trim: float = 5.):
    """
    Wrapper of COLMAP Poisson Surface Reconstruction
    :param: input_file
    :param: output_file
    """
    output, exit_code = sh('colmap poisson_mesher '
                           f'--input_path {input_file} '
                           f'--output_path {output_file} '
                           f'--PoissonMeshing.trim {trim:.1f}')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Poisson Surface Reconstruction run failed!')


def point_triangulator(database_file, image_path, input_model, output_model):
    """
    Wrapper of COLMAP Point Triangulator
    :param: database_file
    :param: image_path
    :param: input_model
    :param: output_model
    """
    output, exit_code = sh('colmap point_triangulator '
                           f'--database_path {database_file} '
                           f'--image_path {image_path} '
                           f'--input_path {input_model} '
                           f'--output_path {output_model}')

    if exit_code != 0:
        print(output)
        raise RuntimeError('COLMAP Poisson Surface Reconstruction run failed!')
