import argparse
import os
import time
import imghdr
import shutil

import numpy as np
from PIL import Image
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


def classify_images(folder_path):
    model_file = '/home/nimbus-pi/mlrasp/server/ml/efficientnet-edgetpu-L_quant.tflite'
    labels_file = '/home/nimbus-pi/mlrasp/server/ml/imagenet_labels.txt'

    labels = read_label_file(labels_file) if labels_file else {}

    interpreter = make_interpreter(model_file)
    interpreter.allocate_tensors()

    # Model must be uint8 quantized
    if common.input_details(interpreter, 'dtype') != np.uint8:
        raise ValueError('Only support uint8 input type.')

    size = common.input_size(interpreter)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if not os.path.isfile(file_path) or imghdr.what(file_path) is None:
            continue

        image = Image.open(file_path).convert('RGB').resize(size, Image.ANTIALIAS)

        params = common.input_details(interpreter, 'quantization_parameters')
        scale = params['scales']
        zero_point = params['zero_points']
        mean = 128.0
        std = 128.0

        if abs(scale * std - 1) < 1e-5 and abs(mean - zero_point) < 1e-5:
            # Input data does not require preprocessing.
            common.set_input(interpreter, image)
        else:
            # Input data requires preprocessing
            normalized_input = (np.asarray(image) - mean) / (std * scale) + zero_point
            np.clip(normalized_input, 0, 255, out=normalized_input)
            common.set_input(interpreter, normalized_input.astype(np.uint8))

        # Run inference
        interpreter.invoke()
        classes = classify.get_classes(interpreter, top_k=1)

        for c in classes:
            output_folder = labels.get(c.id, c.id)
            output_folder_path = os.path.join(folder_path, output_folder)
            os.makedirs(output_folder_path, exist_ok=True)
            output_file_path = os.path.join(output_folder_path, file_name)

            # Move the file instead of copying
            shutil.move(file_path, output_file_path)

            print(f'Moved {file_name} to {output_folder} folder.')


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--folder_path', required=True, help='Path to the folder containing images.')
    args = parser.parse_args()

    classify_images(args.folder_path)


if __name__ == '__main__':
    main()
