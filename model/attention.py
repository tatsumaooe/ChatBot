
import torch
import torch.nn as nn
import torch.nn.functional as F


class SelfAttention(nn.Module):

    def __init__(self, embedding_dim, head_size, max_seq_len):
        super().__init__()

        self.query = nn.Linear(embedding_dim, head_size, bias=False)
        self.key = nn.Linear(embedding_dim, head_size, bias=False)
        self.value = nn.Linear(embedding_dim, head_size, bias=False)

        self.head_size = head_size

        self.register_buffer(
            "mask",
            torch.tril(torch.ones(max_seq_len, max_seq_len))
        )

    def forward(self, x):

        # x: [batch, sequence, embedding]
        B, T, C = x.shape

        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        # Attention scores: [B, T, T]
        scores = Q @ K.transpose(-2, -1)

        scores = scores / (self.head_size ** 0.5)

        # Causal masking
        mask = self.mask[:T, :T]

        scores = scores.masked_fill(
            mask == 0,
            float("-inf")
        )

        # Actual attention weights
        weights = F.softmax(scores, dim=-1)

        # Attention output
        output = weights @ V

        return output, weights


if __name__ == "__main__":

    torch.manual_seed(42)

    model = SelfAttention(
        embedding_dim=64,
        head_size=64,
        max_seq_len=128
    )

    # IMPORTANT: Keep the batch dimension!
    x = torch.randn(2, 5, 64)

    output, weights = model(x)

    print("Input:", x.shape)
    print("Output:", output.shape)
    print("Weights:", weights.shape)

    print("\nAttention weights:")
    print(weights[0])

    print("\nRow sums:")
    print(weights[0].sum(dim=-1))

    print("\nFuture token weights:")
    print(weights[0][0, 1:])
