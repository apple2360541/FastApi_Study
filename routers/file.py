from fastapi import APIRouter,Query,Path,File,UploadFile,Form,Request
from ext import templates
from typing import List
file=APIRouter()


@file.get("/upload_files/")
async def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@file.post("/upload_files/")
async def upload_file(request: Request,
                      file_list: List[bytes] = File(...),
                      file_names: List[UploadFile] = File(...)):
    return templates.TemplateResponse("upload_result.html",
                                      {
                                          "request": request,
                                          "file_sizes": [len(file) for file in file_list],
                                          "file_names": [file.filename for file in file_names],
                                      })


@file.post("/create_file/")
async def create_file(request: Request,
                      file: bytes = File(...),
                      file_type: UploadFile = File(...),
                      notes: str = Form(...)):
    return templates.TemplateResponse("upload_result.html",
                                      {
                                          "request": request,
                                          "file_size": len(file),
                                          "notes": notes,
                                          "file_type": file_type.content_type,
                                      })


@file.get("/create_file")
async def create_file(request: Request):
    return templates.TemplateResponse("create_file.html", {"request": request})