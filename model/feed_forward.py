
import torch
import torch.nn as nn


class FeedForward(nn.Module):

    def __init__(self, embedding_dim=64):
        super().__init__()

        self.network = nn.Sequential(

            # Expand dimensions
            nn.Linear(embedding_dim, embedding_dim * 4),

            # Nonlinear activation
            nn.GELU(),

            # Project back to original dimensions
            nn.Linear(embedding_dim * 4, embedding_dim)
        )

    def forward(self, x):
        return self.network(x)


if __name__ == "__main__":

    torch.manual_seed(42)

    model = FeedForward(embedding_dim=64)

    x = torch.randn(2, 5, 64)

    output = model(x)

    print("Input shape:", x.shape)
    print("Output shape:", output.shape)

    print("\nFeed-forward output:")
    print(output)
