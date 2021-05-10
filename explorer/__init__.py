import shutil

import click
import os

from .explorer import Explorer
from .page import Page
from .utils import slugify


def init_explorer(app, page_funcs, *, root="content", url_root="", page_types={}):
    main_content = Explorer(root=root, url_root=url_root, page_types=page_types)

    app.explorer = main_content

    for page in main_content.pages.values():
        view_func = page_funcs[page.type]
        endpoint = page.endpoint
        endpoint_name = page.endpoint_name

        app.add_url_rule(endpoint, endpoint=endpoint_name, view_func=view_func(page))

    @app.template_filter("slugify")
    def slugify_filter(text):
        return slugify(text)

    @app.context_processor
    def add_content():
        return {
            "main_content": main_content
        }

    @app.cli.command("generate-site")
    @click.argument("html_root", default="output")
    @click.argument("no_server_name", default="true", type=bool)
    def generate_site(html_root, no_server_name):
        if not app.config["SERVER_NAME"]:
            raise Exception("""Server name must be set (not null) to allow url_for to work in request independent
        rendering context""")


        if html_root.startswith("/"):
            output_dir = html_root
        else:
            output_dir = f"{os.getcwd()}/{html_root}"

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        for page in main_content.pages.values():
            view_func = page_funcs[page.type]
            page_content = view_func(page)()
            if no_server_name:
                page_content = page_content.replace(f"http://{app.config['SERVER_NAME']}", "")
            file_name = f"{output_dir}{page.endpoint}/index.html"
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, "w", encoding="utf8") as file:
                file.write(page_content)

        os.system(f"cp -r static {output_dir}")
