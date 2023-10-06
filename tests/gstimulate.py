import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import uuid

# 创建UUID
def generate_uuid():
    return str(uuid.uuid4())
# 创建根元素
def create_root():

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
def create_constant_block(parent, duration):

    constant = ET.SubElement(parent, "Constant")
    base = ET.SubElement(constant, "Base", Version="3")
    core = ET.SubElement(base, "Core", Version="1")
    ET.SubElement(core, "ID").text = generate_uuid()
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
def create_biphasic_pulse_block(parent, amplitude):

    stimulate = ET.SubElement(parent, "BiPhasicPulse")
    base = ET.SubElement(stimulate, "Base", Version="3")
    core = ET.SubElement(base, "Core", Version="1")
    ET.SubElement(core, "ID").text = generate_uuid()
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
def generate_stisequence(root, amplitude_values):
    # 初始值为 100
    total_stimuli_count = 100
    # 添加Primitives节点
    primitives = ET.SubElement(root, "Primitives", Count=str(total_stimuli_count))
    # 计数统计 stimulate 块个数
    sti_count = 0
    # 计数统计 constant 块个数

    con_count = 0

    # 扩大1000倍并四舍五入
    amplitude_values = [round(value * 1000) for value in amplitude_values]

    # 创建10个BigGroup
    for big_group_num in range(0, 10):
        # BigGroup 之间 10s 间隔
        create_constant_block(primitives, 10000000)  # 0幅值，1秒的持续时间
        con_count += 1

        # 每个 BigGroup 包含4个 MinGroup
        for min_group_num in range(0, 4):

            # 每个 MinGroup 包含10个 stimulate
            for stimulate_num in range(0, 10):
                # 创建 <BiPhasicPulse> 块
                create_biphasic_pulse_block(primitives, amplitude_values[stimulate_num])

                # 计数
                sti_count += 1
                # 刺激块之间 1s 间隔
                if sti_count % 10 != 0:
                    create_constant_block(primitives, 1000000)
                    con_count += 1

            # MinGroup 块之间 5s 间隔
            if sti_count % 40 != 0:
                create_constant_block(primitives, 5000000)
                con_count += 1

    Acount = sti_count + con_count
    # 调整 primitives 属性
    primitives.set("Count", str(Acount))


def main():
    # 创建根元素
    root = create_root()

    # 刺激块的幅值数组
    amplitude_values = [900.170137597495, 900.737083886353, 362.976031994147, 900.818806985686,
                        900.006760248206, 900.911469438098, 900.951607022655, 900.502122023043,
                        900.185532317713, 900.784942242060]

    # 生成刺激序列
    generate_stisequence(root, amplitude_values)


    # 使用xml.dom.minidom进行缩进并保存为新的stsd文件
    xml_str = minidom.parseString(ET.tostring(root, encoding="utf-8")).toprettyxml(indent="    ")
    with open("X.stsd", "w", encoding="utf-8") as f:
        f.write(xml_str)


# 调用主函数
if __name__ == "__main__":
    main()
