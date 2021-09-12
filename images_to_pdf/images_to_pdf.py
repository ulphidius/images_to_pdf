from os import listdir
from PIL import Image

def get_relative_path(base_folder, target_folder):
    return '{}/{}'.format(base_folder, target_folder)

def get_list_of_relative_path(base_folder):
    return list(map(lambda name: '{}/{}'.format(base_folder, name), listdir(base_folder)))

def get_list_of_images(list_of_images_path):
    images = list()

    for path in list_of_images_path:
        images.append(Image.open(path))

    return images

def convert_images_color(list_of_images):
    return list(map(lambda image: image.convert('RGB'), list_of_images))

def image_to_pdf(list_of_images, filename):
    list_of_images[0].save(r'{}'.format(filename), save_all=True, append_images=list_of_images)
