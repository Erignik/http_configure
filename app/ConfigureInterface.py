from cmd.CmdFactory import get_cmd_obj
from flask import request
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler
from timer.Conf import TimerConfig


app = Flask(__name__)
CORS(app, resources=r'/*')
app.config.from_object(TimerConfig())


@app.route('/', methods=['GET'])
def get_data():
    return 'hello world'


@app.route('/conf/', methods=['POST'])
def post_data():
    cmd = request.form.get('cmd')
    cmd_obj = get_cmd_obj(cmd)
    ret = False
    info = 'cmd_obj is None...'
    if cmd_obj is not None:
        ret, info = cmd_obj.execute()
    rsp_info = {'ret': ret, 'info': info}
    return jsonify(rsp_info)


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False, host='0.0.0.0', port=7778)
