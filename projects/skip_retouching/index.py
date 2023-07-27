# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from flask import Flask,jsonify,request
from concurrent.futures import ThreadPoolExecutor
import traceback
from projects.skip_retouching.main import Major
from utils.log_utils import logger
from utils import servier_utils as sf
from base import oss_base


executor = ThreadPoolExecutor(1)

app = Flask(__name__)
M = Major()


def _do(trace_id,media_path,out_format,ifoss):
    #异步存储数据库
    try:
        result_path = M.do(trace_id,media_path,out_format,ifoss)
        logger.info(result_path)
    except Exception as e:
        err = traceback.format_exc()
        logger.error(err)
        M.rq.add_progress(M.project_name,trace_id,0,msg=err)
    finally:
        os.remove(media_path)

@app.route('/do',methods=['POST'])
def do():
    r = {}
    try:
        oss_path = sf.getArgsMore('oss_media_path')
        if oss_path is None:raise Exception('oss_media_path is None')
        temp_path = oss_base.download(oss_path)
        out_format = sf.getArgsMore('out_format')
        ifoss = sf.getArgsMore('ifoss')
        trace_id = M.rq.init_progress(M.project_name)
        executor.submit(_do, trace_id,temp_path,out_format,ifoss)
        r['ok'] = 1
        r['trace_id'] = trace_id

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
    app.run(host='0.0.0.0',port=9910,debug=False)