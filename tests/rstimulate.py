import xml.etree.ElementTree as ET
import random
import os
import loguru
import datetime



class XMLRandomNumberFiller:
    def __init__(self, config):
        self.input_file_path = config['input_file_path']
        self.output_file_path = config['output_file_path']
        self.random_min = config['random_min']
        self.random_max = config['random_max']
        self.random_count = config['random_count']
        self.log_file_path = config['log_file_path']

    def setup_logging(self):
        # Create a logs folder if it doesn't exist
        log_folder = os.path.dirname(self.log_file_path)
        os.makedirs(log_folder, exist_ok=True)
        loguru.logger.add(self.log_file_path, rotation="100 MB")  # Rotates the log file when it reaches 10MB

    def fill_random_numbers(self):
        # 解析XML文件
        tree = ET.parse(self.input_file_path)
        root = tree.getroot()

        # 获取到所有的BiPhasicPulse元素
        biphasic_pulse_elements = root.findall(".//BiPhasicPulse")

        # 生成指定数量的随机数
        random_numbers = [random.randint(self.random_min, self.random_max) * 1000 for _ in range(self.random_count)]

        # 遍历BiPhasicPulse元素，填充随机数
        for i, biphasic_pulse_element in enumerate(biphasic_pulse_elements):
            # 获取AmplitudePulse1和AmplitudePulse2元素
            amplitude_pulse1 = biphasic_pulse_element.find('AmplitudePulse1')
            amplitude_pulse2 = biphasic_pulse_element.find('AmplitudePulse2')

            # 将随机数填充到对应元素中
            amplitude_pulse1.text = str(-random_numbers[i])
            amplitude_pulse2.text = str(random_numbers[i])

            loguru.logger.debug(f"num={i+1} : AmplitudePulse1={str(-random_numbers[i])}, AmplitudePulse1={str(random_numbers[i])}")

        # 保存修改后的XML文件
        tree.write(self.output_file_path, encoding='utf-8', xml_declaration=True)


def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    config = {
        'input_file_path': 'stimulate.stsd',
        'output_file_path': 'modified_stimulate.stsd',
        'random_min': 450,
        'random_max': 900,
        'random_count': 120,
        'log_file_path':f"log\\XMLRandomNumberFiller.{timestamp}.log"
    }

    # 创建XMLRandomNumberFiller对象并填充随机数
    xml_filler = XMLRandomNumberFiller(config)
    xml_filler.setup_logging()
    xml_filler.fill_random_numbers()


if __name__ == "__main__":

    main()
