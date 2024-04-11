# -*- coding: utf-8 -*-
import torch

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# Create random Tensors to hold inputs and outputs
x = torch.randn(N, D_in)
y = torch.rand(N, D_out)
print(y[0])

# Use the nn package to define our model and loss function.
model = torch.nn.Sequential(
  torch.nn.Linear(D_in, H),
  torch.nn.ReLU(),
  torch.nn.Linear(H, D_out),
)
loss_fn = torch.nn.MSELoss(reduction='sum')

learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(500):
  y_pred = model(x)

  loss = loss_fn(y_pred, y)
  if t % 100 == 99:
    print(t, loss.item())

  optimizer.zero_grad()
  loss.backward()
  optimizer.step()