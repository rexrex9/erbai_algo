# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from flask import Flask,jsonify,request
import traceback
from projects.progress.major import run,docker_swith
from utils.log_utils import logger
from utils import servier_utils as sf

app = Flask(__name__)


@app.route('/do',methods=['POST'])
def do():
    r = {}
    try:
        trace_id = sf.getArgsMore('trace_id')
        if trace_id is None:raise Exception('trace_id is None')
        project_name = sf.getArgsMore('project_name')
        if project_name is None:raise Exception('project_name is None')

        n,p = run(trace_id,project_name)
        r['progress'] = n
        r['content'] = p
        r['ok'] = 1

    except Exception as e:
        r['ok'] = 0
        err = traceback.format_exc()
        logger.error(err)
        r['error'] = err

    return jsonify(r)



@app.route('/docker_switch',methods=['POST'])
def docker_switch():
    r = {}
    try:
        openorclose = sf.getArgsMore('openorclose')
        project_name = sf.getArgsMore('project_name')
        if project_name is None:raise Exception('project_name is None')
        docker_swith(project_name,openorclose)
        r['ok'] = 1
    except Exception as e:
        r['ok'] = 0
        err = traceback.format_exc()
        logger.error(err)
        r['error'] = err

    return jsonify(r)



@app.route('/hello',methods=['GET'])
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9913,debug=False)