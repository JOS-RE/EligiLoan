import numpy as np
import streamlit as st

import torch
import torch.nn as nn
import torch.nn.functional as F

class LoanModel(nn.Module):
  def __init__(self,in_size,out_size):
    super().__init__()
    self.linear1=nn.Linear(in_size,32)
    self.linear2 = nn.Linear(32, 32)
    self.linear3 = nn.Linear(32, out_size)

  def forward(self,xb):
    out = self.linear1(xb)
    out = F.tanh(out)
    out = self.linear2(out)
    out = F.tanh(out)
    out = self.linear3(out)
    out=F.sigmoid(out)
    return out

class LoanDefaultPrediction(nn.Module):
    __model_path="API/models/eligiloan.pth"

    @st.cache(allow_output_mutation=True)
    def Net():
        model=LoanModel(22,1)
        return model

    @staticmethod
    def load_model():
        model=LoanDefaultPrediction.Net()
        state_dict=torch.load(LoanDefaultPrediction.__model_path,map_location='cpu')
        model=model.load_state_dict(state_dict)
        return model

    @staticmethod
    def to_device(data, device):
        if isinstance(data, (list,tuple)):
            return [to_device(x, device) for x in data]
        return data.to(device, non_blocking=True)    

    @staticmethod
    def predict(x,model):
        x=torch.tensor(x,dtype=torch.float32)
        xb=LoanDefaultPrediction.to_device(x.unsqueeze(0),'cpu')
        yb=model(xb)
        _,preds=torch.max(yb,dim=1)
        return preds   
