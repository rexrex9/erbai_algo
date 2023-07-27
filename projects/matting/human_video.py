from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from os.path import join as osp
from uuid import uuid4
from data import filepath as fp
import cv2
from tqdm import tqdm
import numpy as np
from PIL import Image
from projects.matting.backgroud import BackGround
import os
from base.media_base import BaseClass


class HumanVideo(BaseClass):

    def __init__(self):
        super().__init__()
        self.model = pipeline(Tasks.video_human_matting,model='damo/cv_effnetv2_video-human-matting')
        self.BG = BackGround()
        self.project_name = 'matting'

    def _bocard(self,mask,width):
        anb = []
        for bb in mask:
            nb = []
            for bbb in bb:
                nb.append([bbb] * width)
            anb.append(nb)
        b = np.array(anb)
        return b


    def transparent(self,frame,mask):
        nf = []
        for fi,mi in zip(frame,mask):
            ni = []
            for fj,mf in zip(fi,mi):
                fj = fj.tolist()
                fj.append(int(mf)*255)
                ni.append(fj)
            nf.append(ni)
        nf = np.array(nf,dtype=np.uint8,ndmin=3)
        return nf

    def get_mask(self,video_path):
        temp_video_path = osp(fp.TEMP.VIDEO_DIR, str(uuid4()) + '.mp4')
        result_status = self.model(
            {'video_input_path': video_path,
             'output_path': temp_video_path})
        result = result_status[OutputKeys.MASKS]
        os.remove(temp_video_path)
        return result
    def process_video(self,trace_id,video_path,bg_img=None,bg_video=None,format='mp4',ifbg=True):
        if not ifbg:
            format = 'png_list'
        output_path = self.get_path_name(format)
        mask_results = self.get_mask(video_path)

        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if bg_video:
            cap2 = cv2.VideoCapture(bg_video)
            total_frames2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))

            if total_frames2 < total_frames:
                raise Exception('bg_video frames must be more than video frames')

        if format != 'png_list':
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            videoWriter = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

        count = 0
        while True:
            print('{}/{}'.format(count, total_frames))
            ret, frame = cap.read()
            if not ret: break

            if bg_video:
                ret2, bg_frame = cap2.read()

            mask = mask_results[count]
            frame = self.transparent(frame,mask)

            if ifbg:
                temp_img_path = osp(fp.TEMP.IMAGE_DIR, str(uuid4()) + '.png')
                cv2.imwrite(temp_img_path, frame)
                if bg_video:
                    temp_img_path_bg = osp(fp.TEMP.IMAGE_DIR, str(uuid4()) + '.png')
                    cv2.imwrite(temp_img_path_bg, bg_frame)
                    bg_img = temp_img_path_bg

                img = self.BG.put_together(temp_img_path,bg_img)

                if format == 'png_list':
                    out_path = osp(output_path, '{}.png'.format(count))
                    img.save(out_path)
                else:
                    temp_img_path_in = osp(fp.TEMP.IMAGE_DIR, str(uuid4()) + '.png')
                    img.save(temp_img_path_in)
                    img = cv2.imread(temp_img_path_in)
                    videoWriter.write(img)
                    os.remove(temp_img_path_in)
                os.remove(temp_img_path)
                if bg_video:
                    os.remove(temp_img_path_bg)
            else:

                out_path = osp(output_path, '{}.png'.format(count))
                cv2.imwrite(out_path, frame)

            count += 1
            self.rq.add_progress(self.project_name,trace_id,round(count/total_frames,3)*100)

        cap.release()
        if format != 'png_list':
            videoWriter.release()
        if bg_video:
            cap2.release()


        return output_path

if __name__ == '__main__':
    fip = HumanVideo()
    #p = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/videos/video_matting_test.mp4'
    p = fp.FILE_TEST.VIDEO_13S
    fip.process_video(p,bg_video=fp.FILE_TEST.MAT_BACKGROUND3_MP4,format='mp4')


