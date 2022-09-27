from minio_client import MinioClient
import os


def file_path(path='dummy_file.txt') -> str:
    with open(path, 'w') as f:
        f.write('This is file that uses to test minio client.')
    return path


class TestMinio:
    client = MinioClient()
    new_bucket_name = 'bucket-images'
    object_name = 'dummyTextFile'
    not_existed_object_name = 'dummyTextFile_not_exist'
    file_path = file_path()

    def test_create_bucket(self):
        self.client.make_bucket(self.new_bucket_name)
        buckets_list = self.client.client.list_buckets()
        assert self.new_bucket_name in [b.name for b in buckets_list]

    def test_create_bucket_exist(self):
        self.client.make_bucket(self.new_bucket_name)
        self.client.make_bucket(self.new_bucket_name)
        buckets_list = self.client.client.list_buckets()
        assert self.new_bucket_name in [b.name for b in buckets_list]

    def test_delete_bucket(self):
        self.client.make_bucket(self.new_bucket_name)
        self.client.remove_bucket(self.new_bucket_name)
        buckets_list = self.client.client.list_buckets()
        assert self.new_bucket_name not in [b.name for b in buckets_list]

    def test_delete_bucket_not_exist(self):
        self.client.remove_bucket(self.new_bucket_name)
        self.client.remove_bucket(self.new_bucket_name)
        buckets_list = self.client.client.list_buckets()
        assert self.new_bucket_name not in [b.name for b in buckets_list]

    def test_push_file(self):
        self.client.push_file(self.new_bucket_name, self.object_name, self.file_path)
        self.client.client.stat_object(self.new_bucket_name, self.object_name)

    def test_pull_file(self):
        results = self.client.pull_file(self.new_bucket_name, self.object_name, self.file_path)
        assert results == f'object_name {self.object_name} was saved to {self.file_path}'
        assert os.path.isfile(self.file_path)

    def test_pull_file_not_exist(self):
        result = self.client.pull_file(self.new_bucket_name, self.not_existed_object_name, self.file_path)
        assert result == f'no such object {self.not_existed_object_name}'
