
import torch
import torch.nn as nn

from model.multi_head_attention import MultiHeadAttention
from model.feed_forward import FeedForward


class TransformerBlock(nn.Module):

    def __init__(
        self,
        embedding_dim=64,
        num_heads=4,
        max_seq_len=128
    ):
        super().__init__()

        # Multi-head attention
        self.attention = MultiHeadAttention(
            embedding_dim=embedding_dim,
            num_heads=num_heads,
            max_seq_len=max_seq_len
        )

        # Feed-forward network
        self.feed_forward = FeedForward(
            embedding_dim=embedding_dim
        )

        # Layer normalization
        self.norm1 = nn.LayerNorm(embedding_dim)
        self.norm2 = nn.LayerNorm(embedding_dim)

    def forward(self, x):

        # Attention + residual connection
        normalized = self.norm1(x)

        attention_output, _ = self.attention(normalized)

        x = x + attention_output

        # Feed-forward + residual connection
        normalized = self.norm2(x)

        ff_output = self.feed_forward(normalized)

        x = x + ff_output

        return x


if __name__ == "__main__":

    torch.manual_seed(42)

    model = TransformerBlock(
        embedding_dim=64,
        num_heads=4,
        max_seq_len=128
    )

    x = torch.randn(2, 5, 64)

    output = model(x)

    print("Input shape:", x.shape)
    print("Output shape:", output.shape)

    print("\nModel parameters:")
    total_params = sum(
        p.numel() for p in model.parameters()
    )

    print(f"{total_params:,}")

    print("\nTransformer block:")
    print(model)
