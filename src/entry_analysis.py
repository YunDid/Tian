from DataAnalysis import DataAnalysis

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
        # channel_list = [70,71]
        # numbers = analyzer.statistics_row_data(dataset, channel_list)
        # print("\n".join(numbers))

        # 统计 编号 or 幅值 的出现位点
        # value_list = [0, 1]
        # channels = analyzer.find_values_in_allrows(dataset, value_list)
        # print("\n".join(channels))

        # 奖励刺激验证
        reward_stimulation_lvalues = [768]
        reward_stimulation_rvalues = [256]
        index = [69,70]
        # 100ms
        timsscope_S = 0.0001
        # 采样率
        Sampling_rate = 25000
        other_channel_data = analyzer.get_other_stidata_intime(dataset, index, reward_stimulation_lvalues, reward_stimulation_rvalues, timsscope_S, Sampling_rate)
        analyzer.plot_other_channel_data(other_channel_data)

    # 分析完毕，关闭文件
    analyzer.h5_reader.close_file()

if __name__ == "__main__":
    main()
