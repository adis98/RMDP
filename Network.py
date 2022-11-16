import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
import torch.optim as optim


class DQN(nn.Module):

    def __init__(self, lr, n_inputs, fc1_dims, fc2_dims, n_actions):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(n_inputs, fc1_dims)
        self.fc2 = nn.Linear(fc1_dims, fc2_dims)
        self.fc3 = nn.Linear(fc2_dims, n_actions)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.loss = nn.MSELoss()
        self.optimizer = optim.Adam(self.parameters(), lr=lr)

    def forward(self, state):  # returns the action for a given state
        state = state.type(torch.FloatTensor)
        state = state.to(self.device)
        state = F.leaky_relu(self.fc1(state))
        state = F.leaky_relu(self.fc2(state))
        outputs = F.leaky_relu(self.fc3(state))
        return outputs


class Agent:

    def __init__(self, gamma=0.999, epsilon=0.9, lr=0.01, batch_sz=128, n_actions=5, mapSize=100, max_mem_sz=100000,
                 eps_end=0.01, eps_dec=5e-4):

        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.action_space = [i for i in range(n_actions)]
        self.mem_size = max_mem_sz
        self.batch_sz = batch_sz
        self.mem_cntr = 0
        self.n_inputs = int(((mapSize - 1) * mapSize * 2 * n_actions) + 1 + 7)  # other state inputs are current time and some order params (quantitative ones except capacity)
        self.state_mem = np.zeros((self.mem_size, self.n_inputs), dtype=np.int32)
        self.new_state_mem = np.zeros((self.mem_size, self.n_inputs), dtype=np.int32)
        self.action_mem = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_mem = np.zeros(self.mem_size, np.float32)
        self.terminal_mem = np.zeros(self.mem_size, dtype=np.bool)
        self.policy_nw = DQN(lr, self.n_inputs, 256, 128, n_actions)
        self.policy_nw = self.policy_nw.to(self.policy_nw.device)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_mem[index] = state
        self.action_mem[index] = action
        self.reward_mem[index] = reward
        self.new_state_mem[index] = state_
        self.terminal_mem[index] = done
        self.mem_cntr += 1

    def select_action(self, state):
        sample = np.random.random()
        if sample > self.epsilon:  # take action of network
            state = torch.tensor(state)
            outputs = self.policy_nw.forward(state)
            action = torch.argmax(outputs).item()  # choose the best action, i.e., with highest Q value
        else:
            action = np.random.choice(self.action_space)

        return action

    def learn(self):
        if self.mem_cntr < self.batch_sz:
            return

        self.policy_nw.optimizer.zero_grad()
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_sz, replace=False)
        batch_index = np.arange(self.batch_sz, dtype=np.int32)
        state_batch = torch.tensor(self.state_mem[batch]).to(self.policy_nw.device)
        new_state_batch = torch.tensor(self.new_mem[batch]).to(self.policy_nw.device)
        reward_batch = torch.tensor(self.reward_mem[batch]).to(self.policy_nw.device)
        terminal_batch = torch.tensor(self.terminal_mem[batch]).to(self.policy_nw.device)
        action_batch = self.action_mem[batch]
        q_curr = self.policy_nw.forward(state_batch)[batch_index, action_batch]
        q_next = self.policy_nw.forward(new_state_batch)
        q_next[terminal_batch] = 0.0
        q_target = reward_batch + self.gamma * torch.max(q_next, dim=1)[0]
        loss = self.policy_nw.loss(q_target, q_curr).to(self.policy_nw.device)
        loss.backward()
        self.policy_nw.optimizer.step()
        self.epsilon -= self.eps_dec if self.epsilon > self.eps_min else 0
