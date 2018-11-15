from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from constants import *

def net_init (w = None, b = None):
    n = FeedForwardNetwork()

    inLayer = LinearLayer(inp_layer)
    n.addInputModule(inLayer)

    for i in range(hidden_layers_count):
        hiddenLayer = SigmoidLayer(hidden_layers[i])
        n.addModule(hiddenLayer)

    outLayer = LinearLayer(out_layer)
    n.addOutputModule(outLayer)

    in_to_hidden = FullConnection(inLayer, hiddenLayer)
    hidden_to_out = FullConnection(hiddenLayer, outLayer)

    n.addConnection(in_to_hidden)
    n.addConnection(hidden_to_out)

    n.sortModules()
    return n


n = net_init()
print(n.activate([1, 2, 3, 4, 5, 6]))