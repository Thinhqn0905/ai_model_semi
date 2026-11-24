"""Small causal convolutional quantile forecaster."""
import numpy as np
import torch
from torch import nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv=nn.Conv1d(1,8,3,padding=2)
        self.head=nn.Linear(8,3)
    def forward(self,x):
        z=torch.relu(self.conv(x[:,None,:]))[:,:,:x.shape[1]]
        return self.head(z[:,:,-1])

class TCN:
    def __init__(self, epochs=30, patience=5, seed=0): self.epochs,self.patience,self.seed=epochs,patience,seed
    def fit(self,X,y,X_val=None,y_val=None):
        torch.manual_seed(self.seed); torch.set_num_threads(2)
        X=np.asarray(X,dtype=np.float32); y=np.asarray(y,dtype=np.float32)
        self.mean=float(np.mean(y)); self.scale=max(float(np.std(y)),1e-6)
        self.device='cuda' if torch.cuda.is_available() else 'cpu'
        self.net=Net().to(self.device); opt=torch.optim.Adam(self.net.parameters(),lr=.01)
        x=torch.tensor((X-self.mean)/self.scale,device=self.device); t=torch.tensor((y-self.mean)/self.scale,device=self.device)
        xv=torch.tensor((np.asarray(X_val,dtype=np.float32)-self.mean)/self.scale,device=self.device) if X_val is not None and len(X_val) else x
        yv=torch.tensor((np.asarray(y_val,dtype=np.float32)-self.mean)/self.scale,device=self.device) if X_val is not None and len(X_val) else t
        q=torch.tensor([.1,.5,.9],device=self.device); best=float('inf'); stale=0
        for epoch in range(self.epochs):
            self.net.train()
            for ids in torch.randperm(len(x),device=self.device).split(512):
                e=t[ids,None]-self.net(x[ids]); loss=torch.maximum(q*e,(q-1)*e).mean(); opt.zero_grad(); loss.backward(); opt.step()
            self.net.eval()
            with torch.no_grad():
                e=yv[:,None]-self.net(xv); val=float(torch.maximum(q*e,(q-1)*e).mean())
            if val < best-1e-5: best=val; state={k:v.clone() for k,v in self.net.state_dict().items()}; stale=0
            else: stale+=1
            if stale>=self.patience: break
        self.net.load_state_dict(state); self.best_loss=best; self.epochs_run=epoch+1
        return self
    def predict(self,X):
        self.net.eval(); out=[]
        with torch.no_grad():
            for batch in np.array_split(np.asarray(X,dtype=np.float32),max(1,(len(X)+4095)//4096)):
                out.append(self.net(torch.tensor((batch-self.mean)/self.scale,device=self.device)).cpu().numpy()*self.scale+self.mean)
        a=np.concatenate(out); a.sort(axis=1); return dict(zip(('p10','p50','p90'),a.T))
