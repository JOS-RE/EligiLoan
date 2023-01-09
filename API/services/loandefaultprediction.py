# Commented out IPython magic to ensure Python compatibility.
import warnings

import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from tqdm.notebook import tqdm
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset, random_split,Dataset

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix

warnings.filterwarnings("ignore",category=UserWarning)
SEED=42
# %matplotlib inline

train_df=pd.read_csv("train.csv")
train_df.head()

train_df.drop(['ID','Batch Enrolled','Grade', 'Sub Grade',
       'Employment Duration','Payment Plan', 'Loan Title','Public Record','Collection 12 months Medical', 'Application Type', 'Last week Pay',
       'Accounts Delinquent','Collection 12 months Medical', 'Application Type', 'Last week Pay',
       'Accounts Delinquent'],axis=1,inplace=True)

train_df.head()

train_df.columns

veri_status_mapping={"Not Verified":0,"Verified":1,"Source Verified":2}
train_df["Verification Status"]=train_df["Verification Status"].map(veri_status_mapping)
init_list_mapping={'w':0,'f':1}
train_df['Initial List Status']=train_df['Initial List Status'].map(init_list_mapping)

inputs=train_df.drop('Loan Status',axis=1).values
targets=train_df[['Loan Status']].values
inputs.shape,targets.shape

inputs.shape[1]

targets.shape

"""### Feature Scaling"""

# sc=StandardScaler()
# inputs=sc.fit_transform(inputs)

"""### DataLoader

"""

val_size=10000
train_size=len(inputs)-val_size
dataset=TensorDataset(torch.tensor(inputs,dtype=torch.float32),torch.tensor(targets,dtype=torch.float32))
train_ds,val_ds=random_split(dataset,[train_size,val_size])
len(train_ds),len(val_ds)

batch_size=128

train_loader=DataLoader(train_ds,batch_size,shuffle=True,num_workers=4,pin_memory=True)
val_loader=DataLoader(val_ds,batch_size*2,num_workers=4,pin_memory=True)

def accuracy(outputs, targets):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == targets).item() / len(preds))

class LoanModel(nn.Module):
  def __init__(self,in_size,out_size):
    super().__init__()
    self.linear1=nn.Linear(in_size,32)
    self.linear2 = nn.Linear(32, 32)
    self.linear3 = nn.Linear(32, out_size)

  def forward(self,xb):
    # out = xb.view(xb.size(0), -1)
    out = self.linear1(xb)
    out = F.tanh(out)
    out = self.linear2(out)
    out = F.tanh(out)
    out = self.linear3(out)
    out=F.sigmoid(out)
    return out

  def training_step(self,batch):
    inputs,targets=batch
    out=self(inputs)
    bce_loss = nn.BCELoss()
    loss=bce_loss(out,targets) 
    return loss

  def validation_step(self,batch):
    inputs, targets = batch 
    # print(f"inputs:{inputs}")
    # print(f"targets:{targets}")
    out = self(inputs)
    # print(f"out:{out}")                   
    bce_loss = nn.BCELoss()
    loss=bce_loss(out,targets) 
    # print(f"loss:{loss}")  
    # acc = accuracy(out, targets)           
    # print(f"acc:{acc}")
    return {'val_loss': loss}

  def validation_epoch_end(self, outputs):
    batch_losses = [x['val_loss'] for x in outputs]
    epoch_loss = torch.stack(batch_losses).mean()   
    # batch_accs = [x['val_acc'] for x in outputs]
    # epoch_acc = torch.stack(batch_accs).mean()     
    return {'val_loss': epoch_loss.item()}

  def epoch_end(self, epoch, result):
    print("Epoch [{}], val_loss: {:.4f}".format(epoch, result['val_loss']))

torch.cuda.is_available()

def get_default_device():
  if torch.cuda.is_available():
      return torch.device('cuda')
  else:
      return torch.device('cpu')

device = get_default_device()
device

def to_device(data, device):
  if isinstance(data, (list,tuple)):
      return [to_device(x, device) for x in data]
  return data.to(device, non_blocking=True)

class DeviceDataLoader():
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        return len(self.dl)

train_loader = DeviceDataLoader(train_loader, device)
val_loader = DeviceDataLoader(val_loader, device)

# for xb,yb in train_loader:
#   print("inputs:",xb)
#   print("targets:",yb)
#   break

def evaluate(model, val_loader):
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
    history = []
    optimizer = opt_func(model.parameters(), lr)
    for epoch in range(epochs):
        # Training Phase 
        for batch in train_loader:
            loss = model.training_step(batch)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        # Validation phase
        result = evaluate(model, val_loader)
        model.epoch_end(epoch, result)
        history.append(result)
    return history

input_size=inputs.shape[1]
out_targets=1

model = LoanModel(input_size, out_size=out_targets)
to_device(model, device)

result=evaluate(model,val_loader)
result

n_epochs=20
lr=0.0003

history=fit(n_epochs,lr,model,train_loader,val_loader)

y_pred=[]
y_true=[]

for xb,yb in val_loader:
  output=model(xb)
  output = (torch.max(torch.exp(output), 1)[1]).data.cpu().numpy()
  y_pred.extend(output) # Save Prediction
  yb = yb.data.cpu().numpy()
  y_true.extend(yb) # Save Truth

classes=('0','1')
cf_matrix = confusion_matrix(y_true, y_pred)
df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix) *10, index = [i for i in classes],
                     columns = [i for i in classes])
plt.figure(figsize = (12,7))
sns.heatmap(df_cm, annot=True)

cf_matrix

losses = [r['val_loss'] for r in [result] + history]
plt.plot(losses, '-x')
plt.xlabel('epoch')
plt.ylabel('val_loss')
plt.title('val_loss vs. epochs');

torch.save(model.state_dict(),'eligiloan.pth')

def predict(x,model):
  xb=to_device(x.unsqueeze(0),device)
  yb=model(xb)
  _,preds=torch.max(yb,dim=1)
  return preds

x,target=val_ds[25]
pred=predict(x,model)
print("Input: ", x)
print("Target: ", target.item())
print("Prediction:", pred)