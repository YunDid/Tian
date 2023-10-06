import xml.etree.ElementTree as ET


def compare_xml_files(file1_path, file2_path):
    # 解析两个XML文件
    tree1 = ET.parse(file1_path)
    tree2 = ET.parse(file2_path)

    # 获取两个XML文件的根元素
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # 比较根元素的标签
    if root1.tag != root2.tag:
        print("根元素标签不同:", root1.tag, root2.tag)

    # 比较根元素的属性
    if root1.attrib != root2.attrib:
        print("根元素属性不同:", root1.attrib, root2.attrib)

    # 递归比较子元素
    compare_elements(root1, root2)


def compare_elements(elem1, elem2):
    # 比较元素的标签
    if elem1.tag != elem2.tag:
        print("元素标签不同:", elem1.tag, elem2.tag)

    # 比较元素的属性
    if elem1.attrib != elem2.attrib:
        print("元素属性不同:", elem1.attrib, elem2.attrib)

    # 比较元素的文本内容
    if elem1.text != elem2.text:
        print("元素文本内容不同:", elem1.text, elem2.text)

    # 比较子元素
    children1 = list(elem1)
    children2 = list(elem2)

    if len(children1) != len(children2):
        print("子元素数量不同:", len(children1), len(children2))
    else:
        for child1, child2 in zip(children1, children2):
            compare_elements(child1, child2)


if __name__ == "__main__":
    file1_path = "stimulate.stsd"
    file2_path = "modified_stimulate.stsd"

    compare_xml_files(file1_path, file2_path)
