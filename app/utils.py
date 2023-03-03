import os
import io
import os
from google.cloud import vision
import requests


def image_to_url(image, object_type, object_id, host):
    image_end = image.filename.split('.')[-1]
    image_name = f'{object_type}{object_id}.{image_end}'
    im_path = os.path.join('..', 'resources', 'images', image_name)
    image.save(im_path)
    image_url = f'http://{host}/images/{image_name}'
    return image_url


def image_to_path(image, object_type, object_id):
    image_end = image.filename.split('.')[-1]
    image_name = f'{object_type}{object_id}.{image_end}'
    im_path = os.path.join('..', 'resources', 'images', image_name)
    image.save(im_path)
    return im_path


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\user\\Downloads\\scanimages-1ac6fa1d4963.json"


def scan_image(image):
    # image_path = "ldc_shop_delicacy3_1728x.jpg"
    image_path = image
    # # Initialize the Cloud Vision API client
    client = vision.ImageAnnotatorClient()
    result = {"Status": "", "Title": "", "Author": "", "Genre": "", "Description": ""}
    # Read the image file into memory
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    # Call the text detection API to extract text from the image
    response = client.text_detection(image=vision.Image(content=content))
    try:
        text = response.text_annotations[0].description
        rows = text.split("\n")
    except:
        result["Status"] = "Failed"
        return result
    isbn = ""
    for row in rows:
        if row.startswith("ISBN"):
            isbn = row
    if isbn == "":
        result["Status"] = "Failed"
        return result
    try:
        isbn = isbn.replace("ISBN", "")
    except:
        pass
    try:
        isbn = isbn.replace("-", "")
    except:
        pass
    try:
        isbn = isbn.replace(" ", "")
    except:
        pass
    try:
        isbn = isbn.replace(":", "")
    except:
        pass

    print(isbn)
    # isbn = int(isbn)
    # isbn = "978-1-60309-502-0"

    query = f"isbn:{isbn}"
    base_url = "https://www.googleapis.com/books/v1/volumes"
    # Make the API request
    response = requests.get(base_url, params={"q": query})



    # Check the status code of the response
    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.json()
        print("data is ", data)

        try:
            # Print the book title and author(s)
            title = data["items"][0]["volumeInfo"]["title"]
            authors = data["items"][0]["volumeInfo"]["authors"]
            print("Title:", title)
            result["Title"] = title
            print("Author(s):", ", ".join(authors))
            result["Author"] = authors
            result["Description"] = ""
            result["Genre"] = ""
        except:
            result["Status"] = "Failed"
            return result
        try:
            description = data["items"][0]["volumeInfo"]["description"]
            print("Description: ", description)
            result["Description"] = description
        except:
            pass
        try:
            genre = data["items"][0]["volumeInfo"]["categories"]
            print("Genre: ", genre)
            result["Genre"] = genre
        except:
            pass

    else:
        print("Failed to get book information:", response.status_code)
        result["Status"] = "Failed"
        return result
    result["Status"] = "Success"
    return result
