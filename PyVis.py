import sys
import os
import networkx as nx

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 使用绝对路径
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# graphml_file = os.path.join(base_dir, "output", "8f586bedd33fd43dfe4204413a71337f.graphml")

g = nx.read_graphml("output/8f586bedd33fd43dfe4204413a71337f.graphml")

from pyvis.network import Network

# 使用 PyVis 创建网络图
net = Network(notebook=True)

# 将 NetworkX 图转换为 PyVis 图
net.from_nx(g)

# 显示图
net.show("example.html")