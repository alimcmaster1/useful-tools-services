import os

from sqlalchemy import Table, MetaData, String, Column, ARRAY, TEXT, \
    create_engine, select
from sqlalchemy.engine import ResultProxy


class resourceItem():

    def __init__(self, group: str, item_name: str, links: str,
                 resource_desc: str) -> None:
        self.group = group
        self.item_name = item_name
        self.links = links
        self.resource_desc = resource_desc

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if value is not None:
            self._group = value
        else:
            raise ValueError("Group cannot be None")

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, value):
        if value is not None:
            self._item_name = value
        else:
            raise ValueError("Item Name cannot be None")

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, value):
        if value is not None:
            self._links = value
        else:
            raise ValueError("Links cannot be None")

    @property
    def resource_desc(self):
        return self._resource_desc

    @resource_desc.setter
    def resource_desc(self, value):
        if value is not None:
            self._resource_desc = value
        else:
            raise ValueError("Resource_Desc cannot be None")


class linksTable():
    table_name = "useful_links"
    metadata = MetaData()

    useful_links = Table(table_name, metadata,
                         Column('item_group', String(64)),
                         Column('item_name', String(64)),
                         Column('links', ARRAY(TEXT())),
                         Column("resource_description", TEXT()))


class dbConnection():

    def __init__(self) -> None:
        self._engine = create_engine(os.environ["DB_URL"], echo=True)
        self.conn = self._engine.connect()

    def gen_insert_sql(self, resourceItem):
        insert = linksTable.useful_links.insert().values(
            item_group=getattr(resourceItem, "group"),
            item_name=getattr(resourceItem, "item_name"),
            links=getattr(resourceItem, "links"),
            resource_description=getattr(resourceItem, "resource_desc"))
        return insert

    def gen_delete_sql(self, resourceItem: resourceItem) -> str:
        tb = linksTable.useful_links
        print(resourceItem.item_name)
        print(resourceItem.resource_desc)
        return tb.delete().where(tb.c.item_group == resourceItem.group). \
            where(tb.c.item_name == resourceItem.item_name)

    def select_all(self):
        return self.conn.execute(select([linksTable.useful_links]))

    def execute_ins(self, sql: str) -> ResultProxy:
        return self.conn.execute(sql)
