import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import cv2


# TODO: rewrite visualizer
def visualize_mesh(pcd):
    def load_render_option(vis):
        vis.get_render_option().load_from_json("./data/render_option.json")
        return False

    def save_render_option(vis):
        vis.get_render_option().save_to_json("./data/new_render_option.json")
        return False

    def capture_depth(vis):
        depth = vis.capture_depth_float_buffer()
        plt.imshow(np.asarray(depth))
        plt.show()
        return False

    def capture_image(vis):
        image = vis.capture_screen_float_buffer()
        plt.imshow(np.asarray(image))
        image = (np.asarray(image) * 255).astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite('./data/res.png', image)
        plt.show()
        return False

    key_to_callback = {
        ord("S"): save_render_option,
        ord("R"): load_render_option,
        ord(","): capture_depth,
        ord("."): capture_image
    }
    o3d.visualization.draw_geometries_with_key_callbacks([pcd], key_to_callback, width=640, height=640)
