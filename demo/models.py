import peewee
import peewee_async
from marshmallow import (
    Schema,
    fields,
)

# Connect to a Postgres database.
database = peewee_async.PostgresqlDatabase(
    'aiohttp_demo',
    user='aiohttpdemo_user',
    password='aiohttpdemo_pass'
)


class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField(unique=True)

    class Meta:
        order_by = 'sequence'
        database = database


class Block(BaseModel):
    """Блок контент"""
    name = peewee.CharField(max_length=200)
    video_link = peewee.CharField(max_length=250)
    sequence = peewee.IntegerField()
    view_count = peewee.IntegerField()

    class Meta:
        database = database
        db_table = 'block'


class Page(BaseModel):
    """Страница"""
    name = peewee.CharField(max_length=200)
    slug = peewee.CharField(unique=True)
    sequence = peewee.IntegerField()
    blocks = peewee.ManyToManyField(Block, backref='pages')

    class Meta:
        db_table = 'page'


PageBlock = Page.blocks.get_through_model()


def populate_test_data():
    """Тут создаем Таблицы и заливаем данные"""

    if 'page' in database.get_tables():
        return
    database.create_tables([
        Page,
        Block,
        PageBlock
    ])

    page1 = Page.create(name='First test page', slug='first-test-page', sequence=1)
    page2 = Page.create(name='Second test page', slug='second-test-page', sequence=2)
    page3 = Page.create(name='Third test page', slug='third-test-page', sequence=3)
    page4 = Page.create(name='Fourth test page', slug='fourth-test-page', sequence=4)

    block1 = Block.create(name='First block', video_link='first-blocks-link', sequence=1, view_count=9843)
    block2 = Block.create(name='Second block', video_link='second-blocks-link', sequence=2, view_count=3643)
    block3 = Block.create(name='Third block', video_link='third-blocks-link', sequence=3, view_count=1653)
    block4 = Block.create(name='Fourth block', video_link='fourth-blocks-link', sequence=4, view_count=635)
    block5 = Block.create(name='Fifth block', video_link='fifth-blocks-link', sequence=5, view_count=5432)
    block6 = Block.create(name='Sixth block', video_link='sixth-blocks-link', sequence=6, view_count=7638)
    block7 = Block.create(name='Seventh block', video_link='seventh-blocks-link', sequence=7, view_count=7382)

    data = (
        (page1, (block1, block3, block7)),
        (page2, (block3, block4, block5, block6)),
        (page3, ()),
        (page4, (block3, block4, block5, block6, block7))
    )
    for page, blocks in data:
        for block in blocks:
            PageBlock.create(page=page, block=block)


populate_test_data()


def getPage(slug):
    return Page.select().where(Page.slug == slug).get()


def incrementBlockViewCount(block_id):
    """Добавляем +1 к Block.view_count"""
    query = Block.update(view_count=Block.view_count+1).where(Block.id == block_id)
    query.execute()


def getPageBlocks(page_slug='first-test-page'):
    """Берем все блоки из страницы:"""
    page = Page.select().where(Page.slug == page_slug).get()
    blocks = page.blocks.order_by(Block.sequence)
    for block in blocks:
        incrementBlockViewCount(block.id)
    return blocks


def getPages():
    """Берем все страницы из таблицы"""
    pages = Page.select()
    for page in pages:
        # @TODO: Тут пока захардкодил base_url
        page.slug = 'http://0.0.0.0:8080/page/' + page.slug + '/'
    return pages


class BlockSchema(Schema):
    name = fields.Str(required=True)
    view_count = fields.Integer(required=True)


class PagesBlockNameSchema(Schema):
    name = fields.Str(required=True)


class PageSchema(Schema):
    name = fields.Str()
    slug = fields.Str()


"""
SELECT b.id, b.name, b.video_link, b.sequence, b.view_count 
FROM "block" AS b 
INNER JOIN "page_block_through" AS pb ON (pb.block_id = b.id) 
INNER JOIN "page" AS p ON (pb.page_id = p.id) 
WHERE (pb.page_id = 1) 
ORDER BY b."sequence"
"""
database.close()
