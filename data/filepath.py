from os.path import join as ops
import os

ROOT = os.path.split(os.path.realpath(__file__))[0]

class FILE_TEST():

    FILE_TEST_DIR = ops(ROOT, 'files_test')
    BASE_IMAGE_DIR = ops(FILE_TEST_DIR, 'base_image')
    BASE_VIDEO_DIR = ops(FILE_TEST_DIR, 'base_video')
    FACES_DIR = ops(FILE_TEST_DIR, 'faces')
    MAT_BACKGROUND_DIR = ops(FILE_TEST_DIR, 'mat_background')

    WAV2LIP_AUDIO = ops(FILE_TEST_DIR, 'wav2lip_audio.WAV')
    NOISE_WAV = ops(FILE_TEST_DIR, 'reduce_noise.wav')

    PERSION1=ops(BASE_IMAGE_DIR,'person1.jpg')
    PERSION2=ops(BASE_IMAGE_DIR,'person2.jpg')

    VIDEO_13S = ops(BASE_VIDEO_DIR, 'test_video_13s.mp4')
    VIDEO_27S = ops(BASE_VIDEO_DIR, 'test_video_27s.mp4')
    VIDEO_55S = ops(BASE_VIDEO_DIR, 'test_video_55s.mp4')

    FACE1 = ops(FACES_DIR, 'face1.jpg')
    FACE2 = ops(FACES_DIR, 'face2.jpg')
    FACE3 = ops(FACES_DIR, 'face3.jpg')

    MAT_BACKGROUND1_MP4 = ops(MAT_BACKGROUND_DIR, 'background1.mp4')
    MAT_BACKGROUND2_MP4 = ops(MAT_BACKGROUND_DIR, 'background2.mp4')
    MAT_BACKGROUND3_MP4 = ops(MAT_BACKGROUND_DIR, 'background3.mp4')
    MAT_BACKGROUND_PNG = ops(MAT_BACKGROUND_DIR, 'background.png')
    DEFAULT_GREEN_PNG = ops(MAT_BACKGROUND_DIR, 'default_green.png')

class TEMP():
    FILE_TEST_DIR = ops(ROOT, 'temp')
    AUDIO_DIR = ops(FILE_TEST_DIR, 'audio')
    VIDEO_DIR = ops(FILE_TEST_DIR, 'video')
    IMAGE_DIR = ops(FILE_TEST_DIR, 'image')
    PNG_LIST_DIR = ops(FILE_TEST_DIR, 'png_list')

class RESULTS():
    RESULTS_DIR = ops(ROOT, 'results')
    IMAGE_DIR = ops(RESULTS_DIR, 'image')
    VIDEO_DIR = ops(RESULTS_DIR, 'video')
    AUDIO_DIR = ops(RESULTS_DIR, 'audio')
    PNG_LIST_DIR = ops(RESULTS_DIR,'png_list')
