
from fileinput import filename
import os

from flask import send_file

from app.kenzie import FILES_DIRECTORY


def file_already_exists(filename, extension):
    extension_path = os.path.join(FILES_DIRECTORY, extension)

    return filename  in os.listdir(extension_path)

def upload_image(file):
    filename:str = file.filename

    root, extension = os.path.splitext(filename)
    extension = extension.replace('.', '')

    if file_already_exists(filename, extension):
        raise FileExistsError

    saving_path = os.path.join(FILES_DIRECTORY, extension, filename)
    print(saving_path)
    
    file.save(saving_path)

def download_zip(file_type, compression_ratio):
    output_file = f"{file_type}.zip"
    input_path = os.path.join(FILES_DIRECTORY, file_type)
    output_path_file = os.path.join('/tmp', output_file)

    if os.path.isfile(output_path_file):
        os.remove(output_path_file)

    command = f"zip -r -{compression_ratio} {output_path_file} {input_path}"

    os.system(command)
    return send_file(output_path_file, as_attachment=True)