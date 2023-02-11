import sys

sys.path.append("/src/kosen_ai_app")
from s3 import push_file_to_s3

push_file_to_s3("test_data/image.jpg")
