from .explorer import Explorer
from .page import Page


def init_explorer(app, page_funcs, *, root="content", url_root="", page_types={}):
    main_content = Explorer(root=root, url_root=url_root, page_types=page_types)

    for page in main_content.pages.values():
        view_func = page_funcs[page.type]
        endpoint = page.endpoint
        endpoint_name = page.endpoint_name

        app.add_url_rule(endpoint, endpoint=endpoint_name, view_func=view_func(page))
