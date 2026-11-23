
import torch
import torch.nn as nn
import torch.nn.functional as F


class MultiHeadAttention(nn.Module):

    def __init__(
        self,
        embedding_dim=64,
        num_heads=4,
        max_seq_len=128
    ):
        super().__init__()

        assert embedding_dim % num_heads == 0

        self.num_heads = num_heads
        self.head_size = embedding_dim // num_heads

        self.query = nn.Linear(embedding_dim, embedding_dim)
        self.key = nn.Linear(embedding_dim, embedding_dim)
        self.value = nn.Linear(embedding_dim, embedding_dim)

        self.output_projection = nn.Linear(
            embedding_dim, embedding_dim
        )

        self.register_buffer(
            "mask",
            torch.tril(torch.ones(max_seq_len, max_seq_len))
        )

    def forward(self, x):

        B, T, C = x.shape

        # Generate Q, K, V
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        # Split into multiple heads
        Q = Q.view(B, T, self.num_heads, self.head_size)
        K = K.view(B, T, self.num_heads, self.head_size)
        V = V.view(B, T, self.num_heads, self.head_size)

        # Move head dimension
        Q = Q.transpose(1, 2)
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)

        # Calculate attention scores
        scores = Q @ K.transpose(-2, -1)

        scores = scores / (self.head_size ** 0.5)

        # Causal mask
        mask = self.mask[:T, :T]

        scores = scores.masked_fill(
            mask == 0,
            float("-inf")
        )

        weights = F.softmax(scores, dim=-1)

        # Attention calculation
        output = weights @ V

        # Combine heads
        output = output.transpose(1, 2).contiguous()

        output = output.view(B, T, C)

        # Final projection
        output = self.output_projection(output)

        return output, weights


if __name__ == "__main__":

    torch.manual_seed(42)

    model = MultiHeadAttention(
        embedding_dim=64,
        num_heads=4,
        max_seq_len=128
    )

    x = torch.randn(2, 5, 64)

    output, weights = model(x)

    print("Input:", x.shape)
    print("Output:", output.shape)
    print("Attention weights:", weights.shape)

    print("\nHead 0 attention:")
    print(weights[0, 0])

    print("\nRow sums:")
    print(weights[0, 0].sum(dim=-1))
