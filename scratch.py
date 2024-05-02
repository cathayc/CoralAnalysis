import plotly.graph_objects as go
import numpy as np

pts = np.loadtxt('/Users/cathychang/Desktop/Projects/CoralAnalysis/input/Hydonphora exesa - 1027.txt')
x, y, z = pts.T[1:]

fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z,
                   alphahull=5,
                   opacity=0.4,
                   color='cyan')])
fig.show()