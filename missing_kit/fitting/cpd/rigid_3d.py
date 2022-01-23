from functools import partial

import numpy as np
from matplotlib import pyplot as plt
from pycpd import RigidRegistration


class PatchedCPD(RigidRegistration):
    """
    Patched RigidRegistration class to add more args in callback function
    """

    def register(self, callback=lambda **kwargs: None):
        self.transform_point_cloud()
        while self.iteration < self.max_iterations and self.diff > self.tolerance:
            self.iterate()
            if callable(callback):
                kwargs = {
                    'iteration': self.iteration,
                    'error': self.diff,
                    'X': self.X,
                    'Y': self.TY,
                    'R': self.R,
                    't': self.t,
                    's': self.s,
                    'q': self.q
                }
                callback(**kwargs)

        return self.TY, self.get_registration_parameters()


def normal_callback(iteration, error, s, **kwargs):
    print(f'step: {iteration}, err: {error}, scale: {s}')


def visualize_callback(iteration, error, X, Y, s, q, R, t, ax):
    print(f'step: {iteration}, err: {error}, scale: {s}')
    print(R)
    print(t)
    plt.cla()
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], color='red', label='Target')
    ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], color='blue', label='Source')
    ax.text2D(0.87, 0.92, 'Iteration: {:d}\nQ: {:06.4f}'.format(
        iteration, q), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
              fontsize='x-large')
    ax.legend(loc='upper left', fontsize='x-large')
    plt.draw()
    plt.pause(0.001)


def reg_rigid_3d(source, target, init_trans: np.ndarray = None, visualize: bool = False,
                 tolerance: float = 1e-4, max_iterations: int = 120):
    """
    Register source to target using rigid 3D CPD method
    :param source: `np.ndarray` (n, 3)
    :param target: `np.ndarray` (n, 3)
    :param init_trans: `np.ndarray` (4, 4), note that initial value of R should be positive semi definite
    :param visualize: bool, open a plot for visualization when set to True
    :param max_iterations: max steps
    :param tolerance: max error
    :return: result trans matrix, `np.ndarray` (4, 4)
    """

    # set initial values
    R, t, s = None, None, None
    if init_trans is not None:
        assert init_trans.shape == (4, 4)
        s = np.abs(np.linalg.det(init_trans[0:3, 0:3]))
        R = init_trans[0:3, 0:3].T / s
        t = init_trans[0:3, 3].T

    # setup iteration callback
    if visualize:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        callback = partial(visualize_callback, ax=ax)
    else:
        callback = normal_callback

    # start registration
    reg = PatchedCPD(
        X=target,
        Y=source,
        tolerance=tolerance,
        max_iterations=max_iterations,
        R=R,
        t=t,
        s=s
    )
    reg.register(callback)
    if visualize:
        plt.show()

    # convert to transform matrix
    res = np.zeros((4, 4))
    res[0:3, 0:3] = reg.R.T * reg.s
    res[0:3, 3] = reg.t.T
    res[3, 3] = 1.
    return res
