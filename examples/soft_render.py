import cv2
import matplotlib.pyplot as plt
import numpy as np

from missing_kit.io import load_mesh
from missing_kit.math.transform import apply_matrix
from missing_kit.render import soft_render

if __name__ == '__main__':
    points = load_mesh('./data/meshed-poisson.ply')

    image_width = 1332
    image_height = 1152
    image_dimensions = np.array((image_height, image_width), dtype=np.float64)

    focal_lengths = np.array((2373.046104729776, 2375.5106693944517), dtype=np.float64)
    principal_point = np.array((668.8785376738697, 550.609404815664), dtype=np.float64)

    M_cam = np.asarray([[-0.32296132, 0.51045218, -0.7969533, 0.0464116],
                        [-0.59304238, 0.54709987, 0.59074738, -2.25255],
                        [0.73756133, 0.66341564, 0.12602768, 2.87738],
                        [0., 0., 0., 1.]])
    points = apply_matrix(M_cam, points)

    img = soft_render(points, focal_lengths, principal_point, image_dimensions)
    img = (img * 255).astype(np.uint8)
    img = cv2.dilate(img, kernel=np.ones((10, 10), 'uint8'))
    img = cv2.erode(img, kernel=np.ones((10, 10), 'uint8'))
    plt.imshow(img)
    plt.show()

# 2373.046104729776,2375.5106693944517,668.8785376738697,550.609404815664,0.0,0.0,0.0,0.0
