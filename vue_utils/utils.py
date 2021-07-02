import glob
import os

from PIL import Image



def create_thumbnail(original_file, thb_file_name, size=(100, 60)):
    image = Image.open(original_file)
    image.thumbnail(size)
    image.save(thb_file_name)


def get_image_data(catalog, template, title='Car Photo ', thb_size=(150, 90), prepend_url=''):
    result = []
    filter_ref = catalog + '/' + template
    if os.path.exists(catalog) and os.path.isdir(catalog):
        count = 0
        for infile in glob.glob(filter_ref):
            count += 1
            base_name = os.path.basename(infile)
            path = os.path.dirname(infile)
            thd_name = 'thb_' + base_name
            thd_file = os.path.join(path, thd_name)
            if not os.path.exists(thd_file):
                create_thumbnail(infile, thd_file, thb_size)

            result.append({
                'itemImageSrc': f'{prepend_url}/{base_name}' if prepend_url else base_name,
                'thumbnailImageSrc': f'{prepend_url}/{thd_name}' if prepend_url else thd_name,
                'title': f'{title} {count}'
            })
    return result
