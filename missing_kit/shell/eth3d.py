from typing import List
from dataclasses import dataclass

import numpy as np

from missing_kit.io import save_mesh
from missing_kit.io.meshlab_project import write_meshlab_project
from missing_kit.shell import sh, mkdir


@dataclass
class ETH3DResult:
    tolerances: np.ndarray
    completenesses: np.ndarray
    accuracies: np.ndarray
    f1_scores: np.ndarray


class ETH3DRunner:
    def __init__(self, binary_path: str = 'ETH3DMultiViewEvaluation', work_dir: str = './tmp') -> ETH3DResult:
        """
        Create an ETH3D evaluator instance
        :param binary_path: ETH3DMultiViewEvaluation executable binary path
        :param work_dir: location to store mesh file and meshlab project
        """
        self.main_command = binary_path
        self.work_dir = work_dir

    def compare_mesh(
            self,
            recon_mesh: np.ndarray,
            ground_truth_mesh: np.ndarray,
            tolerances: List[float] = None):
        """
        Compare two aligned meshes
        :param recon_mesh: reconstructed mesh, `np.ndarray` (n, 3)
        :param ground_truth_mesh: ground truth mesh, `np.ndarray` (n, 3)
        :param tolerances: list of non-negative evaluation tolerance values in float
        """
        if tolerances is None:
            tolerances = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
        GT_NAME = 'gt.ply'
        recon_file_path = f'{self.work_dir}/recon.ply'
        gt_file_path = f'{self.work_dir}/{GT_NAME}'
        gt_ml_project_path = f'{self.work_dir}/gt.mlp'

        mkdir(self.work_dir)
        save_mesh(recon_file_path, recon_mesh)
        save_mesh(gt_file_path, ground_truth_mesh)
        write_meshlab_project(gt_ml_project_path, GT_NAME)

        output, exit_code = sh(f'{self.main_command} '
                               f'--tolerances {",".join([str(x) for x in tolerances])} '
                               f'--reconstruction_ply_path {recon_file_path} '
                               f'--ground_truth_mlp_path {gt_ml_project_path}')

        if exit_code != 0:
            print(output)
            raise RuntimeError('ETH3DMultiViewEvaluation run failed!')

        output = output.split('\n')
        for i in range(len(output)):
            if 'Tolerances' in output[i]:
                output = output[i: i + 4]
                break

        return ETH3DResult(
            tolerances=np.fromstring(output[0].split(': ')[1], dtype=float, sep=' '),
            completenesses=np.fromstring(output[1].split(': ')[1], dtype=float, sep=' '),
            accuracies=np.fromstring(output[2].split(': ')[1], dtype=float, sep=' '),
            f1_scores=np.fromstring(output[3].split(': ')[1], dtype=float, sep=' '),
        )
