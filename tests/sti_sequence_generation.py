import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import uuid
import os
import loguru
import datetime

class StiSequenceGeneration:
    def __init__(self, config):

        self.output_file_path = config['output_file_path']
        self.log_file_path = config['log_file_path']
        self.amplitude = config['amplitude_values']
        self.interval_sti = config['interval_sti']
        self.interval_mblock = config['interval_mblock']
        self.interval_bblock = config['interval_bblock']
        self.num_sti = config['num_sti']
        self.num_mblock = config['num_mblock']
        self.num_bblock = config['num_bblock']
        self.encoding = config['encoding']
        self.unit_conv_amp = config['unit_conv_amp']

        self.setup_logging()
        self.root = self.create_root()


    def setup_logging(self):

        # Create a logs folder if it doesn't exist
        log_folder = os.path.dirname(self.log_file_path)
        os.makedirs(log_folder, exist_ok=True)
        loguru.logger.add(self.log_file_path, rotation="100 MB")  # Rotates the log file when it reaches 10MB

    def generate_uuid(self):
        return str(uuid.uuid4())

    def save_to_stsd(self):

        # 使用xml.dom.minidom进行缩进并保存为新的stsd文件
        xml_str = minidom.parseString(ET.tostring(self.root, encoding=self.encoding)).toprettyxml(indent="    ")
        with open(f"{self.output_file_path}", "w", encoding=self.encoding) as f:
            f.write(xml_str)

    # 创建根元素
    def create_root(self):

        root = ET.Element("SettingsStimulator", Version="7")
        # 添加其他属性（与现有stsd文件相同）
        ET.SubElement(root, "StimulusID").text = "1"
        ET.SubElement(root, "SerialNumber").text = "60MEA100_10"
        ET.SubElement(root, "StimulatorProtocol").text = "Step"
        ET.SubElement(root, "OutputMode").text = "Voltage"
        ET.SubElement(root, "OutputRestriction").text = "None"
        ET.SubElement(root, "Tick").text = "20"
        ET.SubElement(root, "Range").text = "12000000"
        ET.SubElement(root, "Resolution").text = "571"
        ET.SubElement(root, "AmplitudeFactor").text = "0"
        ET.SubElement(root, "Offset").text = "0"
        ET.SubElement(root, "Loop").text = "False"
        ET.SubElement(root, "MarkerPortID").text = "-1"
        ET.SubElement(root, "ArtefactSuppression").text = "Blanking"
        ET.SubElement(root, "StartMode").text = "Manual"
        ET.SubElement(root, "TriggerPortID").text = "0"
        ET.SubElement(root, "FeedbackPortID").text = "0"
        ET.SubElement(root, "RetriggerAction").text = "Ignore"
        ET.SubElement(root, "ExternalStimulationElectrodeEnabled").text = "false"

        return root

    # 创建 <Constant> 块
    def create_constant_block(self, parent, duration):

        constant = ET.SubElement(parent, "Constant")
        base = ET.SubElement(constant, "Base", Version="3")
        core = ET.SubElement(base, "Core", Version="1")
        ET.SubElement(core, "ID").text = self.generate_uuid()
        ET.SubElement(core, "PrimitiveType").text = "Constant"
        ET.SubElement(base, "Tick").text = "20"
        ET.SubElement(base, "Range").text = "12000000"
        ET.SubElement(base, "Resolution").text = "571"
        ET.SubElement(base, "Cycles").text = "1"
        ET.SubElement(base, "ISI").text = "0"
        ET.SubElement(base, "MarkerSignal").text = "False"
        ET.SubElement(base, "MarkerSignalRepeat").text = "False"
        ET.SubElement(base, "MarkerSignalOffset").text = "0"
        ET.SubElement(base, "MarkerSignalDuration").text = "200"
        ET.SubElement(constant, "Amplitude").text = "0"
        ET.SubElement(constant, "Duration").text = str(duration)

    # 创建 <BiPhasicPulse> 块
    def create_biphasic_pulse_block(self, parent, amplitude):

        stimulate = ET.SubElement(parent, "BiPhasicPulse")
        base = ET.SubElement(stimulate, "Base", Version="3")
        core = ET.SubElement(base, "Core", Version="1")
        ET.SubElement(core, "ID").text = self.generate_uuid()
        ET.SubElement(core, "PrimitiveType").text = "BiPhasicPulse"
        ET.SubElement(base, "Tick").text = "20"
        ET.SubElement(base, "Range").text = "12000000"
        ET.SubElement(base, "Resolution").text = "571"
        ET.SubElement(base, "Cycles").text = "1"
        ET.SubElement(base, "ISI").text = "0"
        ET.SubElement(base, "MarkerSignal").text = "False"
        ET.SubElement(base, "MarkerSignalRepeat").text = "False"
        ET.SubElement(base, "MarkerSignalOffset").text = "0"
        ET.SubElement(base, "MarkerSignalDuration").text = "200"
        ET.SubElement(stimulate, "AmplitudePulse1").text = str(-amplitude)
        ET.SubElement(stimulate, "DurationPulse1").text = "200"
        ET.SubElement(stimulate, "DurationPause").text = "0"
        ET.SubElement(stimulate, "AmplitudePulse2").text = str(amplitude)
        ET.SubElement(stimulate, "DurationPulse2").text = "200"
        ET.SubElement(stimulate, "DeltaAmplitudePulse1").text = "0"
        ET.SubElement(stimulate, "DeltaDurationPulse1").text = "0"
        ET.SubElement(stimulate, "DeltaDurationPause").text = "0"
        ET.SubElement(stimulate, "DeltaAmplitudePulse2").text = "0"
        ET.SubElement(stimulate, "DeltaDurationPulse2").text = "0"

    # 生成刺激序列
    def generate_stisequence(self):

        # 刺激与控制块计数
        total_stimuli_count = 100
        # 添加 Primitives 节点
        primitives = ET.SubElement(self.root, "Primitives", Count=str(total_stimuli_count))
        # 计数统计 stimulate 块个数
        sti_count = 0
        # 计数统计 constant 块个数
        con_count = 0

        # 转换为 mV 并四舍五入
        amplitude_values = [round(value * self.unit_conv_amp) for value in self.amplitude]

        # 创建10个BigGroup
        for big_group_num in range(0, self.num_bblock):
            # BigGroup 之间 10s 间隔
            self.create_constant_block(primitives, self.interval_bblock)  # 0幅值，1秒的持续时间
            con_count += 1

            # 每个 BigGroup 包含4个 MinGroup
            for min_group_num in range(0, self.num_mblock):

                # 每个 MinGroup 包含10个 stimulate
                for stimulate_num in range(0, self.num_sti):
                    # 创建 <BiPhasicPulse> 块
                    self.create_biphasic_pulse_block(primitives, amplitude_values[stimulate_num])
                    # 计数
                    sti_count += 1
                    # 刺激块之间 1s 间隔
                    if sti_count % self.num_sti != 0:
                        self.create_constant_block(primitives, self.interval_sti)
                        con_count += 1

                # MinGroup 块之间 5s 间隔
                if sti_count % (self.num_sti * self.num_mblock) != 0:
                    self.create_constant_block(primitives, self.interval_mblock)
                    con_count += 1
        # 计数所有 con+amp 字段个数
        Acount = sti_count + con_count

        # 调整 primitives 属性
        primitives.set("Count", str(Acount))

def main():

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # 刺激块的幅值数组
    amplitude_values = [900.170137597495, 900.737083886353, 362.976031994147, 900.818806985686,
                        900.006760248206, 900.911469438098, 900.951607022655, 900.502122023043,
                        900.185532317713, 900.784942242060]
    # 时间间隔 单位：us
    interval_sti = 1000000
    interval_mblock = 5000000
    interval_bblock = 10000000

    # 刺激序列个数
    num_sti = 10
    num_mblock = 4
    num_bblock = 10

    encoding = "utf-8"

    config = {
        'output_file_path': f"StiSequenceGeneration.{timestamp}.stsd",
        'log_file_path':f"log\\StiSequenceGeneration.{timestamp}.log",
        'amplitude_values': amplitude_values,
        'interval_sti': interval_sti,
        'interval_mblock': interval_mblock,
        'interval_bblock': interval_bblock,
        'num_sti': num_sti,
        'num_mblock':num_mblock,
        'num_bblock':num_bblock,
        'encoding': encoding,
        'unit_conv_amp': 1000
    }

    sti_Sequence = StiSequenceGeneration(config)
    sti_Sequence.generate_stisequence()
    sti_Sequence.save_to_stsd()

if __name__ == "__main__":

    main()
