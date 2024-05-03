import os


class CreateDirectory:
    def __init__(self, base_dir: str = 'store'):
        self.base_dir = base_dir

    def create_directory(self):
        if not os.path.exists(f'{self.base_dir}'):
            os.mkdir(self.base_dir)

    def create_subdirectory(self, file_hash):
        self.create_directory()
        subdir = file_hash[:2]
        print(subdir)
        dir_path = os.path.join(self.base_dir, subdir)
        os.mkdir(dir_path)
        return dir_path
