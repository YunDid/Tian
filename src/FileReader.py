import h5py

class H5FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None

    def open_file(self):
        self.file = h5py.File(self.file_path, 'r')

    def close_file(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def read_hdf5_keys(self):
        if self.file is not None:
            keys = list(self.file.keys())
            return keys

    def log_h5_contents(self):
        try:
            # 打开HDF5文件
            if self.file is not None:
                # 递归函数来输出文件内容
                def print_contents(group, indent=""):
                    for name, item in group.items():
                        if isinstance(item, h5py.Group):
                            # 如果是组，输出组名称、属性和子组数量
                            print(f"{indent}Group: {name}")
                            print(f"{indent}  Attributes: {dict(item.attrs)}")
                            print(f"{indent}  Number of Subgroups: {len(item)}")
                            # 递归调用来输出子组内容
                            print_contents(item, indent + "    ")
                        elif isinstance(item, h5py.Dataset):
                            # 如果是数据集，输出数据集名称、数据类型、形状和维度信息
                            print(f"{indent}Dataset: {name}")
                            print(f"{indent}  Datatype: {item.dtype}")
                            print(f"{indent}  Shape: {item.shape}")
                            print(f"{indent}  Dimensions: {item.ndim}")

                # 输出文件内容
                print_contents(self.file)

        except Exception as e:
            print(f"Error: {str(e)}")

    def get_dataset_by_name(self, item_name):
        try:
            # 打开HDF5文件
            if self.file is not None:
                if item_name in self.file:
                    item = self.file[item_name]
                    return item
                else:
                    print(f"Item '{item_name}' not found in the HDF5 file.")
                    return None

        except Exception as e:
            print(f"Error: {str(e)}")
            return None


def main():

    # 创建一个FileReader对象，指定HDF5文件路径
    file_reader = H5FileReader('E:\Data\Train1RawData.h5')
    # 递归输出H5文件结构
    file_reader.log_h5_contents()
    # 获取所有h5内容分支名称
    names_h5 = file_reader.read_hdf5_keys()
    # 根据键值名称获取数据
    dataset = file_reader.get_dataset_by_name(names_h5[0])

if __name__ == "__main__":
    main()
