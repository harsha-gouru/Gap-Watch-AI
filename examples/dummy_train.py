import time
import argparse
import random

def train_model(epochs=3, learning_rate=0.01, feature_dim=100):
    print(f"Starting dummy training...")
    print(f"Parameters: epochs={epochs}, lr={learning_rate}, feature_dim={feature_dim}")

    for epoch in range(1, epochs + 1):
        print(f"Epoch {epoch}/{epochs}")
        # Simulate some work
        time.sleep(random.uniform(0.5, 1.5)) 
        loss = random.uniform(0.1, 0.5) / epoch
        accuracy = 1.0 - loss - random.uniform(0, 0.1)
        print(f"  Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")
    
    print("Dummy training complete.")
    print("Final (simulated) model saved to 'dummy_model.pth'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy ML Training Script")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs.")
    parser.add_argument("--lr", type=float, default=0.01, help="Learning rate.")
    parser.add_argument("--feature-dim", type=int, default=100, help="Dimension of features.")
    # Add any other dummy parameters you might want

    args = parser.parse_args()
    
    train_model(epochs=args.epochs, learning_rate=args.lr, feature_dim=args.feature_dim)
