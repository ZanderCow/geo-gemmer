import os
import io
from werkzeug.datastructures import FileStorage
print("Current Working Directory:", os.getcwd())
with open("static/img/fat-fucker1.png", 'rb') as file:
            file_stream = io.BytesIO(file.read())
            image_1 = FileStorage(stream=file_stream, filename='file.png', content_type='image/png')

            