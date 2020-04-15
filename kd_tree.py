import numpy as np


# kd树结点结构
class KDNode:

    def __init__(self, left=None, right=None, content=None, depth=0):
        # 左子结点
        self.left = left
        # 右子结点
        self.right = right
        # 结点内容
        self.content = content
        # 结点所处kd树深度
        self.depth = depth

    # 递归构造kd树，返回根节点
    @staticmethod
    def create(data_set, depth=0):
        # 递归出口
        if len(data_set) <= 0:
            return None
        else:
            # m: 数据数，n: 数据维度
            m, n = np.shape(data_set)
            # 中位数位置
            median_index = int(m / 2)
            # 比较的轴(l = j mod k + 1)
            target_axis = depth % n
            # 按目标轴排序
            sort_data_set = data_set[np.argsort(data_set[:, target_axis])]
            # 初始化当前节点
            node = KDNode(content=sort_data_set[median_index], depth=depth)
            # 左右子节点
            node.left = KDNode.create(sort_data_set[: median_index], depth=depth+1)
            node.right = KDNode.create(sort_data_set[median_index+1:], depth=depth+1)
            # 返回当前结点
            return node

    # 计算当前节点到目标点的举例
    def calculate_distance(self, target_point):
        return ((self.content - np.array(target_point)) ** 2).sum() ** 0.5


# kd树类
class KDTree:

    def __init__(self, data_set):
        self.root = KDNode.create(data_set)

    # kd树搜索算法
    def search(self, x, n=2):

        # 堆栈记录路径信息
        stack = []
        # 保存目前最近的几个点
        nearest_nodes = []
        nearest_distances = []

        # 找到包含x的叶子结点
        target_node = self.root
        while target_node:
            stack.append(target_node)
            distance = target_node.calculate_distance(x)
            # 判断最近的点是否达到目标值
            if len(nearest_nodes) < n:
                nearest_nodes.append(target_node)
                nearest_distances.append(distance)
            else:
                max_distance = max(nearest_distances)
                # 删除最大值的点存入新值
                if distance < max_distance:
                    del_index = nearest_distances.index(max_distance)
                    del(nearest_distances[del_index])
                    del(nearest_nodes[del_index])
                    nearest_nodes.append(target_node)
                    nearest_distances.append(distance)
            axis = target_node.depth % len(x)
            if x[axis] < target_node.content[axis]:
                target_node = target_node.left
            else:
                target_node = target_node.right

        # 回溯查找最近点
        while stack:
            current_node = stack.pop()
            current_distance = current_node.calculate_distance(x)
            max_distance = max(nearest_distances)
            axis = current_node.depth % len(x)
            # 判断是否需要转到另一区域搜索
            if len(nearest_nodes) < n or abs(x[axis] - current_node.content[axis]) < max_distance:
                # 搜索相反区域
                if x[axis] < current_node.content[axis]:
                    target_node = current_node.right
                else:
                    target_node = current_node.left
                # 重复入栈相同过程
                if target_node:
                    stack.append(target_node)
                    distance = target_node.calculate_distance(x)
                    if len(nearest_nodes) < n:
                        nearest_nodes.append(target_node)
                        nearest_distances.append(distance)
                    else:
                        if distance < max_distance:
                            del_index = nearest_distances.index(max_distance)
                            del (nearest_nodes[del_index])
                            del (nearest_distances[del_index])
                            nearest_nodes.append(target_node)
                            nearest_distances.append(distance)

        nearest_points = [nearest_node.content.tolist() for nearest_node in nearest_nodes]

        return nearest_points, nearest_distances


def main():
    data_set = np.array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
    kd_tree = KDTree(data_set.copy())
    x = input("请输入目标样例x（空格隔开，例“2 3.2”）：").split(" ")
    x = [float(x[i]) for i in range(len(x))]
    n = int(input("请输入最近邻元素个数n："))
    nearest_points, nearest_distances = kd_tree.search(x, n)
    print("最近邻点为：", nearest_points)
    print("距离对应依次为：", nearest_distances)


if __name__ == "__main__":
    main()
