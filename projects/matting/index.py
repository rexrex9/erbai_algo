# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from flask import Flask,jsonify,request
from concurrent.futures import ThreadPoolExecutor
import traceback
from projects.matting.main import Major
from utils.log_utils import logger
from utils import servier_utils as sf
from base import oss_base


executor = ThreadPoolExecutor(1)

app = Flask(__name__)
M = Major()


def _do(trace_id,oss_path,type,ifbg,bg_medio_path,out_format,ifoss,audio_path):
    #异步存储数据库
    temp_bg_medio_path = None
    temp_audio_path = None
    temp_path = None
    try:
        temp_path = oss_base.download(oss_path)

        if bg_medio_path is not None:
            temp_bg_medio_path = oss_base.download(bg_medio_path)

        if audio_path is not None:
            temp_audio_path = oss_base.download(audio_path)

        result_path = M.do(trace_id,temp_path,type,ifbg,temp_bg_medio_path,out_format,ifoss,temp_audio_path)
        logger.info(result_path)
    except Exception as e:
        err = traceback.format_exc()
        logger.error(err)
        M.rq.add_progress(M.project_name,trace_id,0,msg=err)
    finally:
        os.remove(temp_path)
        if temp_bg_medio_path is not None:
            os.remove(temp_bg_medio_path)
        if temp_audio_path is not None:
            os.remove(temp_audio_path)
@app.route('/do',methods=['POST'])
def do():
    r = {}
    try:
        oss_path = sf.getArgsMore('oss_media_path')
        if oss_path is None:raise Exception('oss_media_path is None')

        type = sf.getArgsMore('type')
        if type not in ['human_figure','human_video','universal_figure','png_list']:raise Exception('type must be human_figure or human_video or universal_figure')
        ifbg = sf.getArgsMore('ifbg')
        bg_medio_path = sf.getArgsMore('bg_medio_path')

        out_format = sf.getArgsMore('out_format')
        audio_path = sf.getArgsMore('audio_path')


        ifoss = sf.getArgsMore('ifoss')
        trace_id = M.rq.init_progress(M.project_name)

        executor.submit(_do, trace_id,oss_path,type,ifbg,bg_medio_path,out_format,ifoss,audio_path)
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
    app.run(host='0.0.0.0',port=9909,debug=False)