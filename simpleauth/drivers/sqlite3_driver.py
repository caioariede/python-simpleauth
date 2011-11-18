import sqlite3


def connect(name, *args):
    return sqlite3.connect(name)


def execute(conn, sql, values=None):
    cursor = conn.cursor()
    return cursor.execute(sql, values or ())


def create(conn, sql, values=None):
    cursor = conn.cursor()
    cursor.execute(sql, values or ())
    return cursor.lastrowid


def create_schema(table, *columns):
    return '''CREATE TABLE %(table)s (
id integer primary key autoincrement,
%(columns)s)''' % {
                'table': table,
                'columns': parse_columns(columns)
            }


def parse_columns(columns):
    return ',\n'.join(map(parse_column, columns))


def parse_column(column):
    type_ = parse_column_type(column.type)

    name = column.name
    null = ' null' if column.null else ' not null'
    unique = ' unique' if column.unique else ''
    default = ' default "%s"' % column.default \
                    if column.default \
                    else ''

    return '%(name)s %(type)s%(null)s%(unique)s%(default)s' % {
        'name': name,
        'type': type_,
        'null': null,
        'unique': unique,
        'default': default}


def parse_column_type(type_):
    if type_[0] in ('char', 'varchar'):
        return 'varchar(%d)' % (type_[1],)
    elif type_[0] == 'int':
        return 'integer'
    else:
        return type_[0]
