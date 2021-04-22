from .views import frontend


def setup_routes(app):
    app.router.add_route('GET', '/', frontend.index)
    app.router.add_route('GET', '/page/{slug}/', frontend.page)
    app.router.add_route('GET', '/pages/', frontend.pages)
