from chalice import Chalice
from chalice import NotFoundError
# from chalice import KeyError
import uuid

app = Chalice(app_name='Budget')
app.debug = True


csv_dir = "./csv/"
json_dir = "./json/"


@app.route('/')
def index():
    return {'What is this?': 'This is an OpenSource Framework for public data which can be used to support an AWS Gov Cloud Architecture. ref: https://aws.amazon.com/govcloud-us'}

# why do we want sub-module information - because it is useful?
@app.route('/info/{dept}')
def lookup_dept_info(dept):
    return {
        'General description / purpose & Overview': 'this is the info',
        'this is a secondary element key ' : "this is the value of the secondary element key",
            }


#
@app.route('/dept/{expenses}', methods=['POST','PUT', 'GET'])
def add_inventory(expenses):
    request = app.current_request
    if expenses == 'ALL': return DEPT_EXPENSES
    if request.method == 'PUT' or request.method == 'POST':
        DEPT_EXPENSES[expenses] = request.json_body
    elif request.method == 'GET':
        try:
            return {expenses: DEPT_EXPENSES[expenses]}
        except KeyError:
            raise NotFoundError(expenses)
    return {expenses: DEPT_EXPENSES[expenses]}

