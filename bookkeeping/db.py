import pymysql
import traceback


def __get_db_connect():
    _conn = pymysql.connect(host='127.0.0.1',
                            user='your_db_user',
                            password='db_password',
                            database='db_name',
                            cursorclass=pymysql.cursors.DictCursor)
    return _conn


def run_sql(sql):
    table = DAILYINFO(__get_db_connect())
    table.add_item(sql)


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
        self._tablename = "demo_table_name"


class DAILYINFO(BASEDB):
    #  status: 0-init; 1-confirmed; 2-deleted;

    def list_items(self, username, days=0, **kwargs):
        q = f'SELECT user, transaction_date, item, price, quantity, amount, type, payment, remark FROM {self._tablename} '
        q = q + ' WHERE `user`=%(user)s and `status`=%(status)s '
        q = q + ' AND TO_DAYS(NOW()) - TO_DAYS(transaction_date) <= %(days)s'
        q = q + ' ORDER BY `transaction_date` ASC '
        values = {
            'user': username,
            'days': days,
            'status': 1
        }
        return self._execute_query(q, values)

    def list_items_initdata(self, batch_id, username):
        q = f'SELECT * FROM {self._tablename} '
        q = q + ' WHERE `user`=%(user)s and `status`=%(status)s and `batch_id`=%(batch_id)s '
        q = q + ' ORDER BY `id` ASC '
        values = {
            'batch_id': batch_id,
            'user': username,
            'status': 0
        }
        return self._execute_query(q, values)

    def _execute_query(self, query_sql, values):
        results_list = []
        connection = self._connection
        # cursor = connection.cursor()
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_sql, values)
                print(f"sql:{query_sql}")
            except:
                print("ERROR:[DAILYINFO.list_items][sql:{}]\n{}".format(query_sql, traceback.format_exc()))

            try:
                for result in cursor:
                    results_list.append(result)
                # cursor.close()
            except:
                print("ERROR:[DAILYINFO.list_items]Cannot retrieve query data.\n{}".format(traceback.format_exc()))
        return results_list


    def add_item(self, sql):
        # id = -1
        connection = self._connection
        with connection.cursor() as cursor:
            # Create a new record
            try:
                cursor.execute(sql)
                print(f"execute sql:{sql}")
                # self._log.debug(f"sql:{sql}")
                # id = connection.insert_id()
                print("execute end.")
                connection.commit()
            except Exception as error:
                # self._log.error("ERROR:[DAILYINFO.add_item][sql:{}]\n{}".format(sql, traceback.format_exc()))
                print("ERROR:[DAILYINFO.add_item][sql:{}]\n{}".format(sql, traceback.format_exc()))
                raise error
        # return id

    def update_batch(self, batch_id, username):
        values = {
            'batch_id': batch_id,
            'user': username,
            'updator': username,
            'status': 1
        }
        self._execute_sql(values)

    def delete_item(self, batch_id, username, iid):
        values = {
            'batch_id': batch_id,
            'user': username,
            'id': iid,
            'updator': username,
            'status': 2
        }
        self._execute_update_status(values)

    def _execute_update_status(self, values):
        sql = f"UPDATE {self._tablename} SET `status`=%(status)s, `updator`=%(updator)s" \
              f" WHERE `batch_id`=%(batch_id)s and `user`=%(user)s "
        if id in values:
            sql += " and `id`=%(id)s "

        connection = self._connection
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, values)
                self._log.debug(f"sql:{sql}")
                connection.commit()
            except Exception as error:
                self._log.error("ERROR:[DAILYINFO._execute_update][sql:{}]\n{}".format(sql, traceback.format_exc()))
                raise error


def _debug():
    sql = '''
    INSERT INTO daily_info (item, price, count, amount, user, flag) VALUES ('盒马买牛奶', 3.23, 1, 3.23, 'tester', '支出')
    '''
    run_sql(sql)


if __name__ == '__main__':
    pass
