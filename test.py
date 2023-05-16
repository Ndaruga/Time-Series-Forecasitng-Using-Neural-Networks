import torch
from torch.utils.data import Dataset, DataLoader
from nbeats_pytorch.model import NBeatsNet
import pandas as pd
import numpy as np


# Load the dataset
df = pd.read_csv('weather_data2.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Normalize the data
# norm_df = (df - df.mean()) / df.std()
norm_df = df.copy()
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
cols_to_normalize = ["Temp(°C)", "Humidity (%)", "Pressure (mbar)"]
norm_df[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])

# Define the dataset class
class WeatherDataset(Dataset):
    def __init__(self, data):
        self.data = data.values
        self.len = data.shape[0]
        
    def __getitem__(self, index):
        return self.data[index]
    
    def __len__(self):
        return self.len
    
# Create the dataloader
batch_size = 128
# train_loader = DataLoader(dataset=WeatherDataset(norm_df), batch_size=batch_size, shuffle=True)
train_loader = np.array(DataLoader(dataset=WeatherDataset(df), batch_size=batch_size, shuffle=True))


# Define the model and optimizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NBeatsNet(device=device,
                  stack_types=[NBeatsNet.GENERIC_BLOCK, NBeatsNet.GENERIC_BLOCK],
                  forecast_length=1,
                  thetas_dim=[4, 4],
                  nb_blocks_per_stack=2,
                  hidden_layer_units=128,
                  share_weights_in_stack=False)
optimizer = torch.optim.Adam(model.parameters())

# Train the model
num_epochs = 10
for epoch in range(num_epochs):
    for i, batch in enumerate(train_loader):
        x = batch[:, 1:]  # Exclude the first column (Date)
        y = batch[:, 0]  # Target column is the first column (Temp)
        
        optimizer.zero_grad()
        y_pred = model(x)
        loss = torch.mean((y_pred.squeeze() - y)**2)
        loss.backward()
        optimizer.step()

        print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}')

# Make predictions on the entire dataset
with torch.no_grad():
    model.eval()
    x_test = torch.tensor(norm_df.iloc[:, 1:].values, dtype=torch.float).to(device)
    y_pred = model(x_test).squeeze().detach().cpu().numpy()

# Denormalize the predictions
y_pred = y_pred * df['Temp(°C)'].std() + df['Temp(°C)'].mean()

# Plot the predictions
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Temp(°C)'], label='Actual')
plt.plot(df['Date'], y_pred, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Temp(°C)')
plt.legend()
plt.show()
