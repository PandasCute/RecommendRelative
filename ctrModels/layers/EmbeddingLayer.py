import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F

class EmbeddingLayer(nn.Module):
    def __init__(self, embed_cols, embed_dim, deep_col_idx, cont_cols=None, embed_dropout=0):
        super(EmbeddingLayer, self).__init__()
        self.embed_cols = embed_cols
        self.embed_dim = embed_dim
        self.continue_cols = cont_cols
        self.deep_col_idx = deep_col_idx
        if self.embed_cols is not None:
            self.embed_layers = nn.ModuleDict({'embed_layer_' + col: nn.Embedding(feat_dim, embed_dim)
                                               for col, feat_dim in self.embed_cols})
            self.embed_dropout = nn.Dropout(embed_dropout)
            for tensor in self.embed_layers.values():
                nn.init.xavier_uniform_(tensor.weight)

    def forward(self, X):
        if self.embed_cols is not None:
            x = [self.embed_layers['embed_layer_' + col](X[:, self.deep_col_idx[col]].long())
                 for col, _ in self.embed_cols]
            x = torch.cat(x, 1)
            x = self.embed_dropout(x)
        if self.continue_cols is not None:
            cont_idx = [self.deep_col_idx[col] for col in self.continue_cols]
            x_cont = X[:, cont_idx].float()
            x = torch.cat([x, x_cont], 1) if self.embed_cols is not None else x_cont
        return x