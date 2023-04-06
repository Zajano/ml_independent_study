def makeList(self, node):
    if node == None:
        return []

    return [self.makeList(node.left), node.val, self.makeList(node.right)]


def isSubtree(self, s: TreeNode, t: TreeNode) -> bool:
    if s == None or t == None:
        return False

    s_list = self.makeList(s)
    t_list = self.makeList(t)

    ti = 0
    s_v = s_list[0]
    t_v = t_list[0]

    for i in range(0, len(s_v)):