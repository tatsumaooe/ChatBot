
import torch
import torch.nn as nn


class GPTEmbedding(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int,
        max_seq_len: int
    ):
        super().__init__()

        # Convert token IDs into vectors
        self.token_embedding = nn.Embedding(
            vocab_size,
            embedding_dim
        )

        # Learnable positional embeddings
        self.position_embedding = nn.Embedding(
            max_seq_len,
            embedding_dim
        )

    def forward(self, token_ids):

        batch_size, seq_len = token_ids.shape

        # Token embeddings
        token_vectors = self.token_embedding(token_ids)

        # Position IDs: 0, 1, 2, ..., seq_len-1
        positions = torch.arange(
            seq_len,
            device=token_ids.device
        )

        # Positional embeddings
        position_vectors = self.position_embedding(positions)

        # Combine both embeddings
        output = token_vectors + position_vectors

        return output


if __name__ == "__main__":

    vocab_size = 100
    embedding_dim = 64
    max_seq_len = 128

    model = GPTEmbedding(
        vocab_size,
        embedding_dim,
        max_seq_len
    )

    # Two example sequences, each containing 5 tokens
    sample_tokens = torch.randint(
        0, vocab_size, (2, 5)
    )

    output = model(sample_tokens)

    print("Input shape:", sample_tokens.shape)
    print("Output shape:", output.shape)
    print("Embedding output:")
    print(output)
