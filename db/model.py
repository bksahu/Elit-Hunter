import db.sqlite as sqlite
import time

class ModelSQLite(object):

    def __init__(self):
        self._item_type = 'movies'
        self._connection = sqlite.connect_to_db(sqlite.DB_name)
        #sqlite.create_table(self.connection, self._item_type)

    @property
    def connection(self):
        return self._connection

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(self, title, link, created_at, website, link_id):
        sqlite.insert_one(
            self.connection, title, link, link_id, created_at, website, table_name=self.item_type)

    def create_items(self, items):
        sqlite.insert_many(
            self.connection, items, table_name=self.item_type)

    def getLastId(self, website):
        return sqlite.select_last_id(
            self.connection, website, self.item_type)

    def get_all_items(self):
        items = sqlite.select_all(
            self.connection, self._item_type, 'row_id', True)
        for item in items:
            item['created_at'] = time.ctime(item['created_at']).replace('00:00:00 ', '')
        return items