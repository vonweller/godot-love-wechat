from nicegui import ui, app
from app.layout import layout
from app.settings import settings
from app.project_list import project_list
from pathlib import Path
from app.project import project

static_folder = Path(__file__).parent / "assets"

app.add_static_files("/assets", str(static_folder))


@ui.page("/")
def index_page():
    ui.add_css("::-webkit-scrollbar { display: none; }")
    with layout("home"):
        project_list()


@ui.page("/settings")
def settings_page():
    ui.add_css("::-webkit-scrollbar { display: none; }")
    with layout("setting"):
        settings()


@ui.page("/projects/{id}")
def project_page(id: str):
    ui.add_css("::-webkit-scrollbar { display: none; }")
    with layout("project"):
        project(id)


ui.run(
    port=24512,
    title="Godot Love Wechat",
    window_size=(1024, 768),
    native=True,
    reload=False,
)
