from flask import Flask, request
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from app.kenzie import image
from os import getenv

MAX_CONTENT_LENGTH = int(getenv('MAX_CONTENT_LENGTH'))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH * 1024 * 1024
@app.post('/upload')
def upload():
    files = request.files

    for key, file in files.items():
        
        try:
            image.upload_image(file)
        except FileExistsError:
            return {"msg": "Arquivo já existe"} ,409
        except FileNotFoundError:
            return {"msg": "Extensão não suportada"}, 415

    return {"msg": "Arquivo foi criado com sucesso"} , 201


@app.get('/download-zip')
def download_dir_as_zip():
    file_type = request.args.get("file_extesion")
    compression_ratio = request.args.get("compression_ratio", 6)

    if not file_type:
        return {'msg': 'Query param `file_extesion` é obrigatório'}, 400

    return image.download_zip(file_type, compression_ratio), 200



@app.get('/file')
def file():
    ...

@app.errorhandler(413)
def too_big(error):
    return {"msg": f"Arquivo ultrapassa o limite permitido de {MAX_CONTENT_LENGTH}MB"}, 413