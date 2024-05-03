import os
import shutil

from pathlib import Path

from fastapi import FastAPI, UploadFile

from app.create_directory.create_directory import CreateDirectory
from app.file_hasher.filehasher import FileHasher
from app.find_delete_file import find_and_delete_file

app = FastAPI()


@app.post("/uploadfile")
async def upload_file(file: UploadFile):
    create_dir = CreateDirectory()
    # Можем ли мы сразу хешировать при вызове функции?
    filehasher = FileHasher(file.filename)
    file_hash = filehasher.create_hash()

    create_subdir = create_dir.create_subdirectory(file_hash)

    old_path = Path(f"{create_subdir}/{file.filename}")
    new_path = Path(f"{create_subdir}/{file_hash}")

    with old_path.open("wb+") as file_ob:
        shutil.copyfileobj(file.file, file_ob)

    os.rename(old_path, new_path)

    return {"filename": file.filename, "filehash": file_hash, "subdir": create_subdir, "new_path": new_path}


@app.delete("/delete_file")
async def delete_file(file_name: str):
    dir_path = 'store/'
    if find_and_delete_file(dir_path, file_name):
        return {"message": f"Файл '{file_name}' успешно удален"}
    return {"message": "Файл не найден"}
