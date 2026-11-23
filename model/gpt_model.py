
import torch
import torch.nn as nn

from model.embeddings import GPTEmbedding
from model.transformer_block import TransformerBlock


class GPTLanguageModel(nn.Module):

    def __init__(
        self,
        vocab_size=1000,
        embedding_dim=64,
        num_heads=4,
        num_layers=4,
        max_seq_len=128
    ):
        super().__init__()

        # Token + positional embeddings
        self.embedding = GPTEmbedding(
            vocab_size=vocab_size,
            embedding_dim=embedding_dim,
            max_seq_len=max_seq_len
        )

        # Stack Transformer Blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(
                embedding_dim=embedding_dim,
                num_heads=num_heads,
                max_seq_len=max_seq_len
            )
            for _ in range(num_layers)
        ])

        # Final normalization
        self.final_norm = nn.LayerNorm(embedding_dim)

        # Predict vocabulary token scores
        self.lm_head = nn.Linear(
            embedding_dim,
            vocab_size,
            bias=False
        )

    def forward(self, token_ids, targets=None):

        # Convert token IDs into embeddings
        x = self.embedding(token_ids)

        # Process through Transformer Blocks
        for block in self.blocks:
            x = block(x)

        # Final normalization
        x = self.final_norm(x)

        # Generate vocabulary logits
        logits = self.lm_head(x)

        loss = None

        if targets is not None:

            B, T, V = logits.shape

            loss = nn.functional.cross_entropy(
                logits.reshape(B * T, V),
                targets.reshape(B * T)
            )

        return logits, loss


if __name__ == "__main__":

    torch.manual_seed(42)

    model = GPTLanguageModel(
        vocab_size=1000,
        embedding_dim=64,
        num_heads=4,
        num_layers=4,
        max_seq_len=128
    )

    # Random example token sequences
    input_ids = torch.randint(0, 1000, (2, 10))

    # Random next-token targets for testing
    targets = torch.randint(0, 1000, (2, 10))

    logits, loss = model(input_ids, targets)

    print("Input shape:", input_ids.shape)
    print("Logits shape:", logits.shape)
    print("Loss:", loss.item())

    # Count parameters
    total_params = sum(
        p.numel() for p in model.parameters()
    )

    print("Total parameters:", f"{total_params:,}")
