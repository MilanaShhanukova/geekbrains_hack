from huggingface_hub import snapshot_download

snapshot_download("openai/whisper-large-v3",
                  local_dir='backend/docker/models/whisper-large-v3',
                  local_dir_use_symlinks=False,
                  ignore_patterns=["*.msgpack", "*.bin", "*fp32*", ".gitattributes"],
)
snapshot_download("Open-Orca/Mistral-7B-OpenOrca",
                  local_dir='backend/docker/models/Mistral-7B-OpenOrca',
                  local_dir_use_symlinks=False,
                  ignore_patterns=["Images/*", "configs/*", ".gitattributes"],
)