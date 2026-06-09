import numpy as np 
import matplotlib.pyplot as plt


np.random.seed(42)

X = np.random.randn(100)
y = 3 * X + 2 + np.random.randn(100) * 0.5 



def gradient_descent (X, y, learning_rate=0.01, epochs=1000):
    m = 0.0
    b = 0.0
    n = len(X)
    loss_history = []

    for epoch in range(epochs):
        y_predicted = m * X + b
        loss = (1/n) * (np.sum(y - y_predicted)**2)
        loss_history.append(loss)

        gradient_m = (-2/n) * np.sum(X *(y - y_predicted))
        gradient_b = (-2/n ) * np.sum(y - y_predicted)

        m = m - learning_rate * gradient_m
        b =  b - learning_rate * gradient_b

        if epoch % 100 == 0:
            print(f"Epoch {epoch}: Loss={loss:.4f}, m={m:.4f}, b={b:.4f}")
        
        
    return m, b, loss_history
plt.scatter(X, y, alpha=0.5)
plt.title("Our Dataset")
plt.xlabel('X')
plt.ylabel("y")
plt.show()
m_learned, b_learned, loss_history = gradient_descent(X, y)
print(f"\nTrue values:    m=3, b=2")
print(f"Learned values: m={m_learned:.4f}, b={b_learned:.4f}")

plt.figure(figsize=(10, 4))
plt.plot(loss_history)
plt.title("Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(X, y, alpha=0.5, label="Actual data")
plt.plot(X, m_learned * X + b_learned, color="red", linewidth=2, label=f"Learned line: y={m_learned:.2f}x+{b_learned:.2f}")
plt.title("Gradient Descent Result")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()