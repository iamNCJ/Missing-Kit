from missing_kit.numerics.fitting.cpd import reg_rigid_3d
from missing_kit.io import load_mesh, save_mesh, load_trans
from missing_kit.mesh_process import transform_mesh, simplify_mesh
from missing_kit.shell import mkdir
from missing_kit.shell.eth3d import ETH3DRunner

if __name__ == '__main__':
    OBJECT_NAME = 'egypt_cat'
    BASE_DIR = rf'X:\LIGHT_FIELD_freshmeat\1_24_main_results\{OBJECT_NAME}'
    MODEL_LIST = [
        'undistort_feature_dift_rgb_2',
        'undistort_feature_lambda_1e-2_rgb_2',
        'undistort_feature_test_mask_2',
        'undistort_feature_test_mask_4points_2'
    ]
    PLY_FILE_NAME = 'fused_remove_bottom.ply'
    ALN_FILE_NAME = 'aln_gt.aln'
    ALN_FILE_PATH = rf'{BASE_DIR}\{ALN_FILE_NAME}'
    GT_FILE_PATH = rf'X:\LIGHT_FIELD_freshmeat\gts\{OBJECT_NAME}_no_bottom.ply'
    SAVE_GT_PATH = rf'{BASE_DIR}\gt.ply'
    CPD_NUM_SAMPLE = 1000
    ETH3D_PATH = r'Y:\alignment\meshcmp\meshcmp\ETH3DMultiViewEvaluation.exe'
    RES_PATH = rf'{BASE_DIR}\scores'

    # align one
    gt_mesh = load_mesh(GT_FILE_PATH)
    recon_mesh = load_mesh(rf'{BASE_DIR}\{MODEL_LIST[0]}\{PLY_FILE_NAME}')
    trans = load_trans(ALN_FILE_PATH)
    transformed_gt_points = transform_mesh(gt_mesh, trans)

    # simplify
    simplified_source_points = simplify_mesh(transformed_gt_points, sample_num=CPD_NUM_SAMPLE)
    simplified_target_points = simplify_mesh(recon_mesh, sample_num=CPD_NUM_SAMPLE)

    # CPD reg
    finetuned_trans = reg_rigid_3d(simplified_source_points, simplified_target_points, visualize=True)
    transformed_gt_points = transform_mesh(transformed_gt_points, finetuned_trans)
    save_mesh(SAVE_GT_PATH, transformed_gt_points)

    mkdir(RES_PATH)
    eth3d = ETH3DRunner(
        binary_path=ETH3D_PATH,
        work_dir=RES_PATH
    )
    res = eth3d.compare_mesh(recon_mesh, transformed_gt_points)
    print(res.tolerances)
    print(res.completenesses)
    print(res.accuracies)
    print(res.f1_scores)
