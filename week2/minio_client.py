import minio
from minio.api import S3Error


class MinioClient:
    def __init__(self):
        self.client = minio.Minio(
            endpoint='192.168.2.11:9000',
            access_key='minioadmin',
            secret_key='minioadmin',
            secure=False
        )

    def make_bucket(self, bucket_name: str):
        buckets_list = self.client.list_buckets()
        if bucket_name in [b.name for b in buckets_list]:
            return
        else:
            self.client.make_bucket(bucket_name)

    def remove_bucket(self, bucket_name: str) -> None:
        if self.client.bucket_exists(bucket_name):
            for obj in self.client.list_objects(bucket_name):
                self.remove_object(bucket_name, obj.object_name)
            self.client.remove_bucket(bucket_name)

    def remove_object(self, bucket_name: str, object_name: str) -> None:
        self.client.remove_object(bucket_name, object_name)

    def push_file(self, bucket_name: str, object_name: str, file_path:str):
        self.make_bucket(bucket_name)
        self.client.fput_object(bucket_name, object_name, file_path)

    def pull_file(self, bucket_name, object_name, file_path):
        try:
            self.client.stat_object(bucket_name, object_name)
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return f'no such object {object_name}'
            else:
                raise e
        self.client.fget_object(bucket_name, object_name, file_path)
        return f'object_name {object_name} was saved to {file_path}'



if __name__ == "__main__":
    cl = MinioClient()
    cl.make_bucket('bucket-images')
    # cl.remove_bucket('bucket-images')
    r = cl.client.stat_object('bucket-images', 'dummyTextFile')
    print()



