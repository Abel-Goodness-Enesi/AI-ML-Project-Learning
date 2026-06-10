import numpy as np
import matplotlib.pyplot as plt

def relu(x):
    return np.maximum(0, x)
    
def relu_derivative(x):
    return (x > 0).astype(float)

X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

np.random.seed(42)

W1 = np.random.randn(2, 8) * 0.1
b1 = np.zeros((1, 8))
W2 = np.random.randn(8, 1) * 0.1
b2 = np.zeros((1, 1))


def sigmoid (x):
    return 1/ (1 + np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

def forward(X):
    z1 = np.dot(X, W1) + b1
    a1 = relu(z1)
    z2 = np.dot(a1, W2) +b2
    a2 = sigmoid(z2)
    return z1, a1, z2, a2


def backward (X, y, z1, a1, z2, a2, learning_rate=0.1):
    n = len(X)
    dz2 = a2 - y 
    dW2 = np.dot(a1.T, dz2) /n
    db2 = np.sum(dz2, axis=0, keepdims=True)/n

    da1 = np.dot(dz2, W2.T)
    dz1 = da1 * relu_derivative(z1)
    dW1 = np.dot(X.T, dz1 ) /n
    db1 = np.sum(dz1, axis=0, keepdims=True)/n

    return dW1, db1, dW2, db2

def train(X, y, epochs=10000, learning_rate=0.1):
    global W1, b1, W2, b2
    loss_history = []

    for epoch in range(epochs):
        z1, a1, z2, a2 = forward(X)

        loss = -np.mean(y * np.log(a2 + 1e-8) +(1 - y) * np.log(1 - a2 + 1e-8)) 
        loss_history.append(loss)

        dW1, db1, dW2, db2 = backward(X, y, z1, a1, z2, a2, learning_rate)

        W1 -= learning_rate * dW1
        b1 -= learning_rate *db1
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2

        if epoch % 1000 == 0:
            print(f"Epoch {epoch}: Loss={loss:.4f}")

    return loss_history

loss_history = train(X, y)

z1, a1, z2, a2 = forward(X)
print("\nPredictions:")
for i, (inp, pred, actual) in enumerate(zip(X, a2, y)):
    print(f"Input: {inp} → Predicted: {pred[0]:.4f} → Actual: {actual[0]}")


plt.plot(loss_history)
plt.title("Neural Network Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()