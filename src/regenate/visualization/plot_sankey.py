from pathlib import Path
import plotly.graph_objects as go

def f14(df,out):
    labels=df['boundary'].dropna().astype(str).unique()
    if len(labels)!=1 or not labels[0].strip(): raise ValueError('exactly one boundary required')
    nodes=list(dict.fromkeys(list(df.source)+list(df.target))); fig=go.Figure(go.Sankey(node={'label':nodes},link={'source':[nodes.index(x) for x in df.source], 'target':[nodes.index(x) for x in df.target], 'value':df.value})); fig.add_annotation(text=labels[0],xref='paper',yref='paper',x=1,y=0,showarrow=False); p=Path(out); p.parent.mkdir(parents=True,exist_ok=True)
    fig.write_html(str(p.with_suffix('.html')))
