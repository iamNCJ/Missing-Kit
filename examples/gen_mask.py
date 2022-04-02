import cv2
from tqdm.contrib.concurrent import process_map
from missing_kit.image_process import generate_masked_image
from missing_kit.shell import mkdir


if __name__ == '__main__':
    OBJECT_NAMES = ['paosiqi_new_360', 'metal_360', 'metal_ring_360', 'cone_360']
    for OBJECT_NAME in OBJECT_NAMES:
        mkdir(f'/nfs/minio/new-lightstage-playground/{OBJECT_NAME}/masked_imgs')
        def fn(i):
            image = cv2.imread(f'/nfs/minio/new-lightstage-playground/{OBJECT_NAME}/raw_imgs/orig_{i:03d}.png')
            masked_image = generate_masked_image(image)
            cv2.imwrite(f'/nfs/minio/new-lightstage-playground/{OBJECT_NAME}/masked_imgs/masked_{i:03d}.png', masked_image)
        process_map(fn, range(360), max_workers=16)
