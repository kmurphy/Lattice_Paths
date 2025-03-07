import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def build_path(steps, path):
    """Build path points and other properties of given path."""
    
    label = []
    colors = []

    points = [(0,0)]
    for step in path:
        sp = steps[step]
        colors.append(sp.color)
        label.append(sp.label)
        points.append( (points[-1][0]+sp.x, points[-1][1]+sp.y) )

    return points, colors, "$" + "\\to ".join(label) + "$" 


# minorLocator = MultipleLocator(5)
def draw_path(steps, path, title=None, suptitle=None, y_max=None, ax=None, show=['grid', 'points', 'tunnels']):

    points, colors, label = build_path(steps, path)
    
    if ax is None:
        fig, ax = plt.subplots()

    ax.set_aspect('equal')

    ax.set_frame_on(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    
    x, y = zip(*points)  # Extract x and y coordinates

    for k in range(len(path)):
        ax.plot(x[k:k+2], y[k:k+2], color=colors[k], linewidth=2, zorder=-1)

    y_max = y_max or max(y) or 1
    ax.axis([0, max(x), 0, y_max])

    if 'points' in show:
        ax.scatter(x, y, color='black', s=25, zorder=1, clip_on=False)

    # if 'tunnels' in show:
    #     tunnels = get_tunnels(steps)
    #     for tunnel in tunnels:
    #         height, start, end = tunnel
    #         ax.plot([start+0.5,end+0.5], [height-0.5,height-0.5], '-.', color='navy', lw=1)
    #         pass

    ax.set_xticks(range(max(x)+1), minor=False)
    ax.set_yticks(range(y_max+1), minor=False)

    if 'grid' in show: 
        ax.grid(which='major', alpha=0.3)

    if title:
        plt.title(label)
    plt.text(max(x),y_max, suptitle)
    

def layout_by_feature(df_in, features=[], feature_sort_order=[], row_label=None, head=0):
    """Use given features (1,2,3) compute the row,col position of all paths."""

    if not feature_sort_order: feature_sort_order = [False]*len(features)
    assert len(features)==len(feature_sort_order), "Mismatch in number of features and feature sort orders"

    if row_label is None:
        row_label = "\n".join(["    "*k + f+" %s" for k,f in enumerate(features)])

    df = df_in.sort_values(features+['Path'], ascending=feature_sort_order+[False])

    if len(features)==1:
        df['Row'] = ((df[features[0]] != df[features[0]].shift())).cumsum() - 1
    elif len(features)==2:
        df['Row'] = ((df[features[0]] != df[features[0]].shift()) | (df[features[1]] != df[features[1]].shift())).cumsum() - 1
    elif len(features)==3:
        df['Row'] = ((df[features[0]] != df[features[0]].shift()) | (df[features[1]] != df[features[1]].shift()) | (df[features[2]] != df[features[2]].shift())).cumsum() - 1
    else: 
        print("not done")

    df['Col'] = df.groupby('Row').cumcount()
    df['Row_Len'] = df.groupby('Row')['Col'].transform('max') + 1

    assert df[df.duplicated(subset=['Row','Col'])].shape[0]==0

    row_label += "\n(%s)" 
    df['Row_Label'] = df.apply(
        lambda row: row_label % tuple([row[f] for f in features + ['Row_Len']]), 
        axis=1)

    return df

def layout_paths(ph, df, title_postfix="", show=['grid','points','tunnels']):
    """Use generated layout (row,col) draw (and save) all paths."""

    rows = df['Row'].max() + 1
    cols = df['Col'].max() + 1

    fig, axs = plt.subplots(rows, cols, squeeze=False, figsize=(2.5*cols,1.5*rows))
    print(axs.shape)
    for ax in axs.flat:
        ax.set_frame_on(False)
        ax.set_xticks([])
        ax.set_yticks([])
    
    # determine length of longest label 
    max_length = df.Row_Label.apply(lambda s: max(len(ss) for ss in s.split("\n"))).argmax()
    label = df.Row_Label.values[max_length]
    text_ref = ax.text(0, 0, label)
    fig.canvas.draw()
    bbox = text_ref.get_window_extent(renderer=fig.canvas.get_renderer())
    text_width = bbox.transformed(ax.transData.inverted()).width
    pixel_to_data = ax.transAxes.inverted().transform((bbox.width, 0))[0] - ax.transAxes.inverted().transform((0, 0))[0]
    xlim = ax.get_xlim()
    data_width = pixel_to_data  
    text_ref.remove()

    labels = set()
    for path_idx, path in df.iterrows():
        ax = axs[path.Row][path.Col]
        height = df.query("Row==@path.Row")['Height'].max()
        draw_path(ph.steps, path.Path, ax=ax, y_max=height, show=show)
        label = path.Row_Label
        xoffset = -1.5
        if label not in labels:
            ax.text(-2 - text_width, 0, label, fontsize=8)
            labels.add(label)

    n = len(df.Path.values[0]) if df.shape[0]>0 else 0
    plt.suptitle('%s paths (len %s) %s' % (ph.NAME, n, title_postfix), 
        fontsize=10 if cols<2 else 20 if cols<5 else 30 if cols<10 else 36)

    return fig
    