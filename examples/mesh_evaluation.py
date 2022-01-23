from missing_kit.fitting.cpd import reg_rigid_3d
from missing_kit.io import load_mesh, save_mesh, load_trans
from missing_kit.mesh import transform_mesh, simplify_mesh


def main_pipeline(mesh_file_source, mesh_file_target, aln_file, output_mesh_file, cpd_sample_num: int = 1000):
    # stage 1, load meshes and transform to initial location
    source_points = load_mesh(mesh_file_source)
    target_points = load_mesh(mesh_file_target)
    trans_1, trans_2 = load_trans(aln_file)
    trans = trans_1 @ trans_2  # just to eliminate unit matrix
    transformed_source_points = transform_mesh(source_points, trans)

    # stage 2, simplify mesh
    simplified_source_points = simplify_mesh(transformed_source_points, sample_num=cpd_sample_num)
    simplified_target_points = simplify_mesh(target_points, sample_num=cpd_sample_num)

    # stage 3, run CPD
    finetuned_trans = reg_rigid_3d(simplified_source_points, simplified_target_points, visualize=True)
    transformed_final_points = transform_mesh(transformed_source_points, finetuned_trans)
    save_mesh(output_mesh_file, transformed_final_points)


if __name__ == '__main__':
    main_pipeline(
        mesh_file_source='./data/egypt/egypt_no_bottom.ply',
        mesh_file_target='./data/egypt/fullon_180.ply',
        aln_file='./data/egypt/alignment_egypt_180.aln',
        output_mesh_file='./data/egypt/egypt_gt.ply'
    )
