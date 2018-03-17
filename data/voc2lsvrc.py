#!/usr/bin/python
# -*- coding=utf-8 -*-

from xml.etree.ElementTree import ElementTree, Element


def read_xml(in_path):
      # return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=False)


def if_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


def get_node_by_keyvalue(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


def change_node_properties(nodelist, kv_map, is_delete=False):

    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):

    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text
def create_node(tag, property_map, content):
    '''''新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element


def del_node(pnode,nodename):
    node1 = pnode.findall(nodename)  # A. 找到父节点
    if len(node1) == 0:
        return tree
    pnode.remove(node1[0])
    return pnode

def add_child_node(nodelist, element):
    '''''给一个节点添加子节点
       nodelist: 节点列表
       element: 子节点'''
    for node in nodelist:
        node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag):
    '''''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        del parent_node.attrib['path']
        parent_node.remove()
        # children = parent_node.getchildren()
        # for child in children:
        #     if child.tag == tag :
        #         parent_node.remove(child)
import os
if __name__ == "__main__":
    # 1. 读取xml文件
    path = r"/home/sbd/data/train/labmouse_recdata/VOCdevkit2007/VOC2007/Annotations"
    new_path = r'/home/sbd/data/train/ILSVRC2015/Annotations/DET/train'

    #del:  segmented  owner size->depth  <object>	pose	truncated	difficult
    files = os.listdir(path)
    for i,file in enumerate(files):
        tree = read_xml(os.path.join(path,file))
        nodes = tree.findall("filename")# A. 找到父节点
        jpeg_name = file.split('.')[0]+'.jpg'
        change_node_text(nodes,jpeg_name)

        del_node(tree.getroot(), "path")
        del_node(tree.getroot(), "segmented")
        del_node(tree.getroot(), "owner")

        n_size=tree. findall("size")
        del_node(n_size[0], "depth")

        n_obj = tree.findall("object")
        del_node(n_obj[0], "pose")
        del_node(n_obj[0], "truncated")
        del_node(n_obj[0], "difficult")

        write_xml(tree,os.path.join(new_path,file))# 6. 输出到结果文件

        if i==10:
            # break
            pass


    # B. 通过属性准确定位子节点
    # result_nodes = get_node_by_keyvalue(nodes, {"name": "BProcesser"})
    # C. 修改节点属性
    # change_node_properties(result_nodes, {"age": "1"})
    # # D. 删除节点属性
    # change_node_properties(result_nodes, {"value": ""}, True)
    #
    # # 3. 节点修改
    # # A.新建节点
    # a = create_node("person", {"age": "15", "money": "200000"}, "this is the firest content")
    # # B.插入到父节点之下
    # add_child_node(result_nodes, a)
    #
    # # 4. 删除节点
    # # 定位父节点
    # del_parent_nodes = find_nodes(tree, "processers/services/service")
    # # 准确定位子节点并删除之
    # target_del_node = del_node_by_tagkeyvalue(del_parent_nodes, "chain", {"sequency": "chain1"})
    #
    # # 5. 修改节点文本
    # # 定位节点
    # text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency": "chain3"})