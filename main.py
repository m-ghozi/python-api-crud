import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

app = FastAPI()


class Blog(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str


blogs = []


@app.post("/blogs", response_model=Blog)
def create_blog(blog: Blog):
    blog.id = uuid4()
    blogs.append(blog)
    return blog


@app.get("/blogs", response_model=list[Blog])
def list_blog():
    return blogs


@app.put("/blog/{blog_id}", response_model=Blog)
def update_blog(blog_id: UUID, blog_update: Blog):
    for idx, blog in enumerate(blogs):
        if blog_id == blog_id:
            updated_blog = blog.copy(update=blog_update.dict(exclude_unset=True))
            blogs[idx] = updated_blog
            return updated_blog

    raise HTTPException(status_code=404, detail="Blog not found")


@app.delete("/blogs/{blog_id}", response_model=Blog)
def delete_blog(blog_id: UUID):
    for idx, blog in enumerate(blogs):
        if blog.id == blog_id:
            return blogs.pop(idx)

    raise HTTPException(status_code=404, detail="Blog not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
