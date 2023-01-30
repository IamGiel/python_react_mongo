from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from typing import List

from models.models import Book, BookUpdate
from dependencies.dependencies import get_token_header

from config.database import TEST_DB

router = APIRouter(
    prefix="/books",
    tags=["books"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/a-book", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_book

@router.get("/all-books", response_description="List all books", response_model=List[Book])
def list_books(request: Request):
    books = list(TEST_DB.db["books"].find(limit=100))
    if(books):
        return books
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"SOME ERROR on list all books")

@router.get("/find-book-by/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.put("/update-book-by{id}", response_description="Update a book", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    book = {k: v for k, v in book.dict().items() if v is not None}
    if len(book) >= 1:
        update_result = request.app.database["books"].update_one(
            {"_id": id}, {"$set": book}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.delete("/delete-book-by/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")