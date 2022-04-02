import cv2
import numpy as np
import onnxruntime as rt
from PIL import Image


def preprocess(image: Image) -> np.ndarray:
    """
    Preprocess the image to be used as input to the model
    ref: https://github.com/xuebinqin/U-2-Net/blob/master/data_loader.py
    :param image: [H, W, C]
    :return: [1, 3, 320, 320], NCHW
    """
    image = image.resize((320, 320))
    image = np.array(image)
    tmp_img = np.zeros((image.shape[0], image.shape[1], 3))
    image = image / np.max(image)
    if image.shape[2] == 1:
        tmp_img[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
        tmp_img[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
        tmp_img[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
    else:
        tmp_img[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
        tmp_img[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
        tmp_img[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225
    return np.moveaxis(tmp_img[np.newaxis], -1, 1)


def infer_u2net(input_image: np.ndarray) -> Image:
    """
    Infer the U^2-Net model via ONNX Runtime
    :param input_image: [1, 3, 320, 320], NCHW
    :return: mask in PIL.Image grayscale format
    """
    sess = rt.InferenceSession('./missing_kit/image_process/u2net.quant.onnx', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    pred_onx = sess.run([output_name], {input_name: input_image.astype(np.float32)})[0]
    pred_onx = (pred_onx - np.min(pred_onx)) / (np.max(pred_onx) - np.min(pred_onx))
    mask = Image.fromarray((pred_onx[0, 0] * 255).astype(np.uint8), mode='L')
    return mask


def generate_image_mask(image: np.ndarray) -> np.ndarray:
    """
    Generate image's mask using U^2-Net
    :param image: [H, W, C]
    :return: [H, W], in grayscale (0~255)
    """
    image = Image.fromarray(image)
    input_image = preprocess(image)
    mask = infer_u2net(input_image)
    mask = mask.resize(image.size, Image.BILINEAR)
    return np.array(mask)


def generate_masked_image(image: np.ndarray, threshold: int = 128, process_kernel: int = 10) -> np.ndarray:
    """
    Generate masked image using U^2-Net
    :param image: [H, W, C]
    :param threshold: threshold for mask (0~255)
    :param process_kernel: kernel size for dilate and erode
    :return: [H, W, C]
    """

    mask = generate_image_mask(image)

    # process mask
    mask[mask > threshold] = 255
    mask[mask <= threshold] = 0
    mask = cv2.dilate(mask, kernel=np.ones((process_kernel, process_kernel), np.uint8))
    mask = cv2.erode(mask, kernel=np.ones((process_kernel, process_kernel), np.uint8))
    mask = cv2.erode(mask, kernel=np.ones((process_kernel, process_kernel), np.uint8))
    mask = cv2.dilate(mask, kernel=np.ones((process_kernel, process_kernel), np.uint8))

    # generate masked image
    image = Image.fromarray(image)
    mask = Image.fromarray(mask, mode='L')
    return np.array(Image.composite(image, Image.fromarray(np.zeros_like(image)), mask))
