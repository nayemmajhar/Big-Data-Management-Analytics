import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import animation, rc
from IPython.display import HTML, Image
import networkx as nx
import pandas as pd
import numpy as np
import random
import dgl

rc('animation', html='html5')


def load_data():
    num_samples = 1000
    xlst=[]

    for _ in range(0,num_samples):
        a = random.randrange(0,2)
        b = random.randrange(0,2)
        xlst.append([a,b])
    xarr = np.array(xlst)

    raw_data_ = {}
    for op in ['AND', 'OR', 'XOR']:
        ylst=[]

        for idx in range(0,num_samples):
            if op == 'AND': y = xarr[idx,0] & xarr[idx,1]
            if op == 'OR':  y = xarr[idx,0] | xarr[idx,1]
            if op == 'XOR': y = xarr[idx,0] ^ xarr[idx,1]
            ylst.append([y])
        yarr = np.array(ylst)

        raw_data_[op] = {
            'X': xarr,
            'Y': yarr
        }
    return raw_data_

def plot_dataset(raw_data_, dataset):
    data = np.concatenate((raw_data_[dataset]['X'], raw_data_[dataset]['Y']), axis=1)
    cols = ['g' if y==1 else 'r' for y in data[:][:,2]]
    pd.DataFrame({'X1': data[:][:,0], 'X2': data[:][:,1]}).plot.scatter(x='X1',y='X2', c=cols, style='o', title=f'{dataset} - actual')
    plt.show()
    
def predict(w, x):
    bias = w[0]
    z = np.sum(w[1:].T * x) + bias
    y_pred = 1. if z > 0 else 0
    return y_pred

def predict_mlp(w1, w2, x):
    
    bias = w1[0]
    z1 = np.sum(w1[1:].T * x) + bias
    z1 = z1.reshape(1,len(z1))

    a1 = 1. / (1. + np.exp(-z1))
    
    bias = w2[0]
    z2 = np.sum(w2[1:].T * a1) + bias
    z2 = z2.reshape(1,len(z2))

    y_pred = 1. / (1. + np.exp(-z2))
    
    return y_pred
    
def test_slp(w, wrong_classifications, losses, title):

    pd.DataFrame({'wrong_classifications': wrong_classifications}).plot(ylim=0)
    plt.show()    
    pd.DataFrame({'loss': losses}).plot(ylim=0, title='loss per epoch')
    plt.show()
    
    num_rand=3000
    x_extra = [[0.,0.],[1.,0.],[0.,1.],[1.,1.]]
    x1,x2,y,lbl=[],[],[],[]
    for i in range(num_rand):
        x1.append(random.random())
        x2.append(random.random())
        input_ = np.array([x1[-1],x2[-1]])
        y_ = predict(w, input_)
        y.append(y_)
        col = 'g' if y_ == 1. else 'r'
        lbl.append(col)
    
    for x in x_extra:
        x1.append(x[0])
        x2.append(x[1])
        input_ = np.array([x1[-1],x2[-1]])
        y_ = predict(w, input_)
        y.append(y_)
        col = 'g' if y_ == 1. else 'r'
        lbl.append(col)
    
    pd.DataFrame({'X1': x1, 'X2': x2}).plot.scatter(x='X1',y='X2',c=lbl,title=title)
    plt.show()
    
    ins = np.array([[0,0],[0,1],[1,0],[1,1]])
    for input_ in ins:
        y_ = predict(w, input_)
        print(f'{input_} -> {y_ }')

def test_mlp(w1, w2, losses, title):
   
    pd.DataFrame({'loss': losses}).plot(ylim=0, title='loss per epoch')
    plt.show()
    
    num_rand=3000
    threshold = 0.5
    x_extra = [[0.,0.],[1.,0.],[0.,1.],[1.,1.]]
    x1,x2,y,lbl=[],[],[],[]
    for i in range(num_rand):
        x1.append(random.random())
        x2.append(random.random())
        input_ = np.array([x1[-1],x2[-1]])
        y_ = predict_mlp(w1, w2, input_).ravel()[0]
        y.append(y_)
        col = 'g' if y_ >= threshold else 'r'
        lbl.append(col)
    
    for x in x_extra:
        x1.append(x[0])
        x2.append(x[1])
        input_ = np.array([x1[-1],x2[-1]])
        y_ = predict_mlp(w1, w2, input_).ravel()[0]
        y.append(y_)
        col = 'g' if y_ >= threshold else 'r'
        lbl.append(col)
    
    pd.DataFrame({'X1': x1, 'X2': x2}).plot.scatter(x='X1',y='X2',c=lbl,title=title)
    plt.show()
    pd.DataFrame({'y_': y}).plot(title='y_pred errors')
    plt.show()
    
    ins = np.array([[0,0],[0,1],[1,0],[1,1]])
    for input_ in ins:
        y_ = predict_mlp(w1, w2, input_).ravel()[0]
        print(f'{input_} -> {y_ }')
    
def plot_graphs(nx_G, predictions, losses, wrong_classifications):
    
    def membership_check(node_idx, y_pred_node_membership):
            # True labels of the group each student (node) unded up in. Found via the original paper
            y_true_node_memberships = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

            community_node_indexes = np.argwhere(y_pred_node_membership == y_true_node_memberships).T.ravel()
            return (node_idx in community_node_indexes)
    
    def draw(epoch):
    
        pos = {}
        colors = []
        class_colors = {0: '#6098d7', 1: '#FF0000', 2: '#E8E8E8'} # 0: true 0, 1: true 1, 2: wrong prediction

        for node_idx in range(0, len(nx_G.nodes())):

            pos[node_idx] = predictions[epoch][node_idx].numpy()
            predicted_class_idx = pos[node_idx].argmax()
            
            color_idx = (2, predicted_class_idx)[membership_check(node_idx, predicted_class_idx)]
            
            
            colors.append(class_colors[color_idx])

        ax.cla()
        ax.axis('off')
        ax.set_title(f'Epoch: {epoch} Loss: {round(losses[epoch],3)} Wrong: {wrong_classifications[epoch]}')
        nx.draw_networkx(nx_G.to_undirected(), pos, node_color=colors,
                with_labels=True, node_size=300, linewidths=0.5, width=0.3, font_size=8, ax=ax)
    
    
    fig = plt.figure(dpi=150)
    fig.clf()
    ax = fig.subplots()
    plt.close()
    
    anim = animation.FuncAnimation(fig, draw, frames=len(predictions), interval=200)
    
    return anim

def load_graph_data():
    # All 78 edges are stored in two numpy arrays. One for source endpoints
    # while the other for destination endpoints.
    src = np.array([1, 2, 2, 3, 3, 3, 4, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10, 11, 12, 12, 13, 13, 13, 13, 16, 16, 17, 17, 19, 19, 21, 21, 25, 25, 27, 27, 27, 28, 29, 29, 30, 30, 31, 31, 31, 31, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33])
    dst = np.array([0, 0, 1, 0, 1, 2, 0, 0, 0, 4, 5, 0, 1, 2, 3, 0, 2, 2,  0,  4,  5,  0,  0,  3,  0,  1,  2,  3,  5,  6, 0, 1, 0, 1, 0, 1, 23, 24, 2, 23, 24, 2, 23, 26, 1, 8, 0, 24, 25, 28, 2, 8, 14, 15, 18, 20, 22, 23, 29, 30, 31, 8, 9, 13, 14, 15, 18, 19, 20, 22, 23, 26, 27, 28, 29, 30, 31, 32])
    # Edges are directional in DGL; Make them bi-directional.
    u = np.concatenate([src, dst])
    v = np.concatenate([dst, src])
    # Construct a DGLGraph
    return dgl.DGLGraph((u, v))