import os
def image_to_url(image, object_type ,object_id, host):
    image_end = image.filename.split('.')[-1]
    image_name = f'{object_type}{object_id}.{image_end}'
    im_path = os.path.join('..','resources', 'images', image_name)
    image.save(im_path)
    image_url = f'http://{host}/images/{image_name}'
    return image_url