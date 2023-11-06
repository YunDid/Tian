import matplotlib.pyplot as plt
from FileReader import H5FileReader
import numpy as np

class DataAnalysis:
    def __init__(self, h5_file_path):
        self.h5_reader = H5FileReader(h5_file_path)

    def get_dataset(self, dataset_name):
        dataset = self.h5_reader.get_dataset_by_name(dataset_name)
        if dataset is not None:
            return dataset
        else:
            print(f"Dataset '{dataset_name}' not found in the HDF5 file.")
            return None

    def plot_dataset_mer(self, dataset, rows=None):
        data = dataset[()]
        num_rows, num_samples = data.shape
        if rows is not None:
            rows_to_plot = rows
        else:
            rows_to_plot = list(range(num_rows))

        plt.figure(figsize=(10, 5))

        for row in rows_to_plot:
            color = np.random.rand(3, )  # 随机选择颜色 rgb
            plt.plot(data[row, :], color=color, label=f'Row {row}')

        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Dataset Plot")
        plt.legend(loc='upper right')
        plt.show()

    def plot_dataset_subplot(self, dataset, rows=None):
        data = dataset[()]
        num_rows, num_samples = data.shape
        if rows is not None:
            rows_to_plot = rows
        else:
            rows_to_plot = list(range(num_rows))

        # 创建一个1x2的子图布局
        fig, axes = plt.subplots(1, 3, figsize=(12, 5))

        for i, row in enumerate(rows_to_plot):
            color = np.random.rand(3, )  # 随机选择颜色 rgb
            ax = axes[i]  # 获取当前子图

            ax.plot(data[row, :], color=color, label=f'Row {row}')
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.set_title(f"Dataset Plot for Row {row}")
            ax.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    def plot_dataset_sep(self, dataset, rows=None):
        data = dataset[()]
        num_rows, num_samples = data.shape
        if rows is not None:
            rows_to_plot = rows
        else:
            rows_to_plot = list(range(num_rows))

        for row in rows_to_plot:
            plt.figure(figsize=(10, 5))  # 创建一个新画布
            color = np.random.rand(3, )  # 随机选择颜色 rgb
            plt.plot(data[row, :], color=color, label=f'Row {row}')
            plt.xlabel("Time")
            plt.ylabel("Amplitude")
            plt.title(f"Dataset Plot - Row {row}")
            plt.legend(loc='upper right')
            plt.show()

    def plot_dataset_trash(self, dataset, rows=None):
        data = dataset[()]
        num_rows, num_samples = data.shape
        if rows is not None:
            rows_to_plot = rows
        else:
            rows_to_plot = list(range(num_rows))

        # 计算子图的行数和列数，以确保能容纳所有曲线
        num_subplots = len(rows_to_plot)
        num_cols = 2  # 假设每行显示两个子图
        num_rows_subplot = (num_subplots + num_cols - 1) // num_cols

        # 创建子图
        fig, axes = plt.subplots(num_rows_subplot, num_cols, figsize=(10, 5 * num_rows_subplot))

        for i, row in enumerate(rows_to_plot):
            color = np.random.rand(3, )  # 随机选择颜色 rgb
            ax = axes[i // num_cols, i % num_cols]  # 获取当前子图
            ax.plot(data[row, :], color=color, label=f'Row {row}')
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.set_title(f'Row {row}')
            ax.legend(loc='upper right')

        # 删除未使用的子图
        for i in range(num_subplots, num_rows_subplot * num_cols):
            fig.delaxes(axes[i // num_cols, i % num_cols])

        plt.tight_layout()
        plt.show()


    def statistics_row_data(self, dataset, row_indices):
        # 统计不同通道出现的所有编号
        rawdata = dataset[()]
        result = []

        for row_index in row_indices:
            rowdata = rawdata[row_index, :]  # 获取指定行的数据
            data_counts = {}  # 用于存储数据值和计数的字典

            for value in rowdata:
                if value in data_counts:
                    data_counts[value] += 1
                else:
                    data_counts[value] = 1

            # 格式化结果为字符串，包括通道信息
            result.extend([f'row:{row_index} num:{key} count:{value}' for key, value in data_counts.items()])

        return result

    def find_values_in_allrows(self, dataset, values):
        # 获取数据数组
        rawdata = dataset[()]
        num_rows = rawdata.shape[0]

        # 创建字典来存储 num 值和它们的行和计数
        num_dict = {}

        for value in values:
            # 遍历数据集的每一行
            for row_index in range(num_rows):
                row_data = rawdata[row_index, :]
                count = np.count_nonzero(row_data == value)

                if count > 0:
                    # 如果 num 值已经在字典中，更新行和计数
                    if value not in num_dict:
                        # 否则，创建一个新的字典项
                        num_dict[value] = {'rows': [row_index], 'count': count}
                        continue

                    num_dict[value]['rows'].append(row_index)
                    num_dict[value]['count'] += count

        # print(num_dict)

        # 生成输出字符串
        result = [f'num:{key} row:{", ".join(map(str, value["rows"]))} count:{value["count"]}' for key, value in
                  num_dict.items()]

        return result

    def plot_other_channel_data(self, other_channel_data):
        num_channels = len(other_channel_data)
        num_rows = int(np.sqrt(num_channels))
        num_cols = (num_channels + num_rows - 1) // num_rows

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))
        plt.subplots_adjust(hspace=1, wspace=1)  # 调整子图之间的间距

        for i, (channel, data) in enumerate(other_channel_data.items()):
            ax = axes[i // num_cols, i % num_cols]  # 获取当前子图
            time = range(len(data))  # 横坐标为样本数

            ax.plot(time, data, color='b')  # 绘制通道数据
            # 标识出每个通道的数据中每个刺激时刻的第一个数据点（红色圆点）
            # for idx, sublist in enumerate(data):
            #     ax.scatter(time[idx] * 25, sublist[0], color='r', marker='o', s=50)
            #     print(f"idx:{idx} sublistFirstEle:{sublist[0]}")

            ax.set_title(f'Channel {channel}')  # 设置子图标题

        for i in range(num_channels, num_rows * num_cols):
            fig.delaxes(axes[i // num_cols, i % num_cols])  # 删除未使用的子图

        plt.show()

    def get_other_stidata_intime(self, dataset, index, reward_stimulation_lvalues, reward_stimulation_rvalues, timsscope_S, Sampling_rate):
        rawdata = dataset[()]

        # 获取数据维度
        num_channels, num_samples = rawdata.shape

        # 提取两个通道的数据
        channel_left_data = rawdata[index[0], :]
        channel_right_data = rawdata[index[1], :]

        # 获取左右轮奖励刺激对应的时间位点
        reward_stimulation_indices_left = np.where(np.isin(channel_left_data, reward_stimulation_lvalues))[0]
        reward_stimulation_indices_right = np.where(np.isin(channel_right_data, reward_stimulation_rvalues))[0]

        # 合并左右两个通道的奖励刺激时间位点
        unique_reward_stimulation_indices = np.union1d(reward_stimulation_indices_left,reward_stimulation_indices_right)

        # 获取时间跨度
        tims_dimension = int(timsscope_S * 25000)

        # 获取刺激时刻处其他通道后 100ms 的数据
        other_channel_data = {}
        for i in range(num_channels):
        # for i in range(4):
            if i not in [index[0], index[1]]:
                channel_data = rawdata[i, :]

                channel_data_after_stimulation = [channel_data[index1:index1 + tims_dimension] for index1 in
                                                  unique_reward_stimulation_indices]

                other_channel_data[i] = channel_data_after_stimulation

        #         channel_data_after_stimulation = []
        #
        #         for timeindex in unique_reward_stimulation_indices:
        #             # 特殊标识奖励刺激时刻
        #             is_index = timeindex in unique_reward_stimulation_indices
        #             data = channel_data[timeindex:timeindex + tims_dimension]
        #             channel_data_after_stimulation.append((data, is_index))
        #
        #         other_channel_data[i] = channel_data_after_stimulation

        return other_channel_data

def main():
    # 创建一个DataPlotter对象，指定HDF5文件路径
    h5_file_path = 'E:\Data\Train1RawData.h5'
    analyzer = DataAnalysis(h5_file_path)
    # 打开文件
    analyzer.h5_reader.open_file()
    # 递归输出H5文件结构
    analyzer.h5_reader.log_h5_contents()
    # 获取所有h5内容分支名称
    names_h5 = analyzer.h5_reader.read_hdf5_keys()
    # 根据键值名称获取数据
    dataset = analyzer.get_dataset(names_h5[0])

    # 如果成功获取到dataset，则可以进行数据分析
    if dataset is not None:

        # 绘制指定通道的数据
        rows_to_plot = [0,1,2]
        # analyzer.plot_dataset_subplot(dataset,rows_to_plot)

        # 统计指定通道额数据出现次数
        channel_list = [69, 71]
        numbers = analyzer.statistics_row_data(dataset, channel_list)
        print("\n".join(numbers))

        # 统计 编号 or 幅值 的出现位点
        # value_list = [0, 1]
        # channels = analyzer.find_values_in_allrows(dataset, value_list)
        # print("\n".join(channels))

    # 分析完毕，关闭文件
    analyzer.h5_reader.close_file()


if __name__ == "__main__":
    main()
