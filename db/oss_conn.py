import oss2
import os

class Paths():

    ROOT = "algo_medias/"
    VIDEO = "algo_medias/video/"
    IMAGE = "algo_medias/image/"
    AUDIO = "algo_medias/audio/"


class OssConn(object):

    def __init__(self):
        END_POINT = "https://oss-cn-shanghai.aliyuncs.com/"
        BUCKET1 = "bxn-rby"
        accessKeyId = "LTAI4G2eU6XFw22REmf583pA"
        accessKeySecret = "CjMN0XvoLjYNW82bQCGkY5URA7cIjK"
        auth = oss2.Auth(accessKeyId, accessKeySecret)
        self.bucket = oss2.Bucket(auth, END_POINT, BUCKET1)

    def upload(self, local_file, object_name):
        oss2.resumable_upload(self.bucket, object_name, local_file)

    def download(self, object_name, local_file):
        oss2.resumable_download(self.bucket, object_name, local_file)

    def delete(self, object_name):
        self.bucket.delete_object(object_name)

    def upload_dir(self, local_dir, object_dir):
        for file in os.listdir(local_dir):
            self.upload(local_dir +'/'+ file, object_dir + '/'+file)


if __name__ == '__main__':
    image_path = 'algo_medias/test_files/person1.jpg'
    #测试一下
    oc = OssConn()
    oc.bucket.get_bucket_info()
    #oc.upload("run.txt", "algo_medias/test.txt")
    oc.download(image_path, "a.jpg")