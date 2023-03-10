import pymysql
import traceback
from cfg.cfg import DB_HOST, DB_USER, DB_USER_PWD
from cfg.cfg import DB_BOOKKEEPING_NAME, DB_BK_TABLE_NAME
import sqlparse as sqlparse


def __get_db_connect():
    _conn = pymysql.connect(host=DB_HOST,
                            user=DB_USER,
                            password=DB_USER_PWD,
                            database=DB_BOOKKEEPING_NAME,
                            cursorclass=pymysql.cursors.DictCursor)
    return _conn


def _varify_sql(sql_insert, tn=None):
    formatted_sql = sqlparse.format(sql_insert, identifier_case='upper')

    if tn is not None and not sql_insert.strip().startswith(f"INSERT INTO {tn}"):
        return False
    parsed = sqlparse.parse(formatted_sql)
    if len(parsed) != 1:
        print(len(parsed))
        return False
    x = y = 0
    for each_token in parsed[0].tokens:
        if each_token.value == 'INSERT':
            x = x + 1
        if each_token.value.startswith('VALUES'):
            y = y + 1
    if x != 1 or y != 1:
        return False
    return True


def run_sql(sql, verbose):
    if not _varify_sql(sql, tn=DB_BK_TABLE_NAME):
        if verbose:
            print(f"不正确的SQL:[{sql}]")
        return
    else:
        table = DAILYINFO(__get_db_connect())
        table.execute_insert(sql)
    if verbose:
        print("execute end.")


def query_transactions(username, days):
    table = DAILYINFO(__get_db_connect())
    return table.list_items(username=username, days=days)


def query_from_db(batch_id, username):
    table = DAILYINFO(__get_db_connect())
    return table.list_items_initdata(batch_id=batch_id, username=username)


def confirm(batch_id, username):
    table = DAILYINFO(__get_db_connect())
    return table.update_batch(batch_id=batch_id, username=username)


def delete(batch_id, username, iid):
    table = DAILYINFO(__get_db_connect())
    return table.delete_item(batch_id=batch_id, username=username, iid=iid)


class BASEDB(object):
    def __init__(self, connection, log=None):
        self._connection = connection
        self._tablename = DB_BK_TABLE_NAME


class DAILYINFO(BASEDB):
    #  status: 0-init; 1-confirmed; 2-deleted;

    def list_items(self, username, days=0, **kwargs):
        q = f'SELECT user, transaction_date, item, price, quantity, amount, type, payment, remark FROM {self._tablename} '
        q = q + ' WHERE `username`=%(username)s and `status`=%(status)s '
        q = q + ' AND TO_DAYS(NOW()) - TO_DAYS(transaction_date) <= %(days)s'
        q = q + ' ORDER BY `transaction_date` ASC '
        values = {
            'username': username,
            'days': days,
            'status': 1
        }
        return self._execute_query(q, values)

    def list_items_initdata(self, batch_id, username):
        q = f'SELECT * FROM {self._tablename} '
        q = q + ' WHERE `username`=%(username)s and `status`=%(status)s and `batch_id`=%(batch_id)s '
        q = q + ' ORDER BY `id` ASC '
        values = {
            'batch_id': batch_id,
            'username': username,
            'status': 0
        }
        return self._execute_query(q, values)

    def _execute_query(self, query_sql, values):
        results_list = []
        connection = self._connection
        # cursor = connection.cursor()
        with connection.cursor() as cursor:
            try:
                print(f"execute sql:{query_sql}")
                cursor.execute(query_sql, values)
            except:
                print("ERROR:[DAILYINFO.list_items][sql:{}]\n{}".format(query_sql, traceback.format_exc()))

            try:
                for result in cursor:
                    results_list.append(result)
                # cursor.close()
            except:
                print("ERROR:[DAILYINFO.list_items]Cannot retrieve query data.\n{}".format(traceback.format_exc()))
        return results_list

    def execute_insert(self, sql):
        # id = -1
        connection = self._connection
        with connection.cursor() as cursor:
            # Create a new record
            try:
                print(f"execute sql:{sql}")
                cursor.execute(sql)
                # id = connection.insert_id()
                connection.commit()
            except Exception as error:
                # self._log.error("ERROR:[DAILYINFO.add_item][sql:{}]\n{}".format(sql, traceback.format_exc()))
                print("ERROR:[DAILYINFO.add_item][sql:{}]\n{}".format(sql, traceback.format_exc()))
                raise error
        # return id

    def update_batch(self, batch_id, username):
        values = {
            'batch_id': batch_id,
            'username': username,
            'updator': username,
            'status': 1
        }
        self._execute_sql(values)

    def delete_item(self, batch_id, username, iid):
        values = {
            'batch_id': batch_id,
            'username': username,
            'id': iid,
            'updator': username,
            'status': 2
        }
        self._execute_update_status(values)

    def _execute_update_status(self, values):
        sql = f"UPDATE {self._tablename} SET `status`=%(status)s, `updator`=%(updator)s" \
              f" WHERE `batch_id`=%(batch_id)s and `username`=%(username)s "
        if id in values:
            sql += " and `id`=%(id)s "

        connection = self._connection
        with connection.cursor() as cursor:
            try:
                print(f"execute sql:{sql}")
                cursor.execute(sql, values)
                connection.commit()
            except Exception as error:
                print("ERROR:[DAILYINFO._execute_update][sql:{}]\n{}".format(sql, traceback.format_exc()))
                raise error


if __name__ == '__main__':
    pass
