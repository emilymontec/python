from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data import users, tasks

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def login_view(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    username = username.strip()
    password = password.strip()

    if username in users and users[username] == password:

        # 🔥 redirección según rol
        if username == "admin":
            redirect_url = "/admin"
        else:
            redirect_url = "/home"

        response = RedirectResponse(redirect_url, status_code=302)
        response.set_cookie("user", username)
        return response

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": "Usuario o contraseña incorrectos."
        }
    )

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    user = request.cookies.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user}
    )

@app.get("/tasks", response_class=HTMLResponse)
def view_tasks(request: Request):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "tasks": tasks
        }
    )

@app.post("/tasks")
def add_task(title: str = Form(...)):
    tasks.append({
        "title": title,
        "status": "pending"
    })
    return RedirectResponse("/tasks", status_code=302)

@app.get("/tasks/delete/{index}")
def delete_task(index: int):
    if 0 <= index < len(tasks):
        tasks.pop(index)

    return RedirectResponse("/tasks", status_code=302)


@app.get("/tasks/toggle/{index}")
def toggle_task(index: int):
    if 0 <= index < len(tasks):
        if tasks[index]["status"] == "pending":
            tasks[index]["status"] = "done"
        else:
            tasks[index]["status"] = "pending"

    return RedirectResponse("/tasks", status_code=302)

@app.get("/admin", response_class=HTMLResponse)
def admin_view(request: Request):
    user = request.cookies.get("user")

    if user != "admin":
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "user": user}
    )

@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("user")
    return response

# Para ejecutar: uvicorn main:app --reload