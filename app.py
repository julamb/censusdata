from flask import Flask, request, render_template
import sqlite3, json


# Init app
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = sqlite3.connect(app.config['DB_FILE'])


# Fetch column names
query = db.execute("SELECT * FROM `%s`" % app.config['TABLE'])
columns = [column[0] for column in query.description]

if app.config['VARIABLE'] not in columns:
    raise ValueError("Parameter VARIABLE should be one of the column names")


# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', columns=columns)


# Results endpoint
@app.route('/results', methods=['GET'])
def get_top_results():
    key = request.args.get('key', '')
    query = db.execute("SELECT `{0}`, COUNT(`{0}`) as c, AVG(`{1}`) FROM `{2}` GROUP BY `{0}` ORDER BY c DESC".format(key, app.config['VARIABLE'], app.config['TABLE'], app.config['LIMIT']))
    results = query.fetchall()

    if len(results) > app.config['LIMIT']:
        ignored_results = results[app.config['LIMIT']+1:]
        results = results[:app.config['LIMIT']]
        ignored_list = ','.join(["'%s'" % r[0] for r in ignored_results if r[1] is not 0])
        query = db.execute("SELECT COUNT(`{0}`) FROM `{1}` WHERE `{0}` IN ({2})".format(key, app.config['TABLE'], ignored_list))
        num_ignored_rows = query.fetchone()[0]
        num_ignored_results = len(ignored_results)

    else:
        num_ignored_rows = 0
        num_ignored_results = 0

    return json.dumps({'results': [{'value': r[0], 'count': r[1], 'average': r[2]} for r in results if r[1] is not 0],
                       'ignored_values': num_ignored_results,
                       'ignored_rows': num_ignored_rows})


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])