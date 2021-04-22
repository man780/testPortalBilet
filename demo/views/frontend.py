from aiohttp_jinja2 import template
from demo.models import getPageBlocks, getPages, getPage, BlockSchema, PageSchema
from aiohttp import web


@template('index.html')
async def index(request):
    pages = getPages()
    return {'pages': pages}


def pages(request):
    pages = getPages()
    pageSchema = PageSchema(many=True)
    serializedPages = pageSchema.dump(list(pages))
    return web.json_response({'pages': serializedPages})


def page(request):
    slug = request.match_info.get('slug')
    page = getPage(slug)
    pageBlocks = getPageBlocks(slug)

    pageSchema = PageSchema()
    blockSchema = BlockSchema(many=True)

    serializedPageBlocks = blockSchema.dump(list(pageBlocks))
    serializedPage = pageSchema.dump(page)

    return web.json_response({'page': {
        'page': serializedPage,
        'blocks': serializedPageBlocks,
    }})
