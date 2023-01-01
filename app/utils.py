def image_to_url(image, host):
    image_end = image.filename.split('.')[-1]
    image_name = f'{id}.{image_end}'
    image.save('resources/images/' + image_name)
    image_url = f'http://{host}/{image_name}'
    return image_url