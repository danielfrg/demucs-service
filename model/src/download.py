import torch as th
from demucs import pretrained

from config import settings


th.hub.set_dir(settings.models)

model_id = "mdx_extra_q"
pretrained.get_model(model_id)
