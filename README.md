# ONNX-Based Technical Document Summarization (Docker Deployment)

## Project Overview
This project demonstrates a reproducible AI deployment pipeline for summarizing technical engineering documents using a pretrained **T5-small** transformer model exported to the **ONNX** format.

To improve deployment efficiency, the ONNX model was further optimized using **dynamic quantization**, significantly reducing model size and improving CPU inference performance while maintaining comparable summarization quality.

The entire inference pipeline is containerized with Docker to ensure consistent execution across operating systems and hardware environments.


---

## Features
- Pretrained T5-small summarization model
- ONNX export for portable inference
- Dynamic INT8 quantization for reduced model size
- Docker container for reproducible deployment
- Command-line interface supporting arbitrary input text
- Cross-platform execution (Windows, macOS, Linux)

---

## Repository Contents
Dockerfile
requirements.txt
infer.py
models/ (quantized ONNX model + tokenizer files)
README.md

---

## Option 1 (Recommended): Pull Prebuilt Docker Image
Instead of building locally, you may pull the container directly from Docker Hub:

```bash
docker pull gaoshuaige/t5-onnx-summarizer
```

## Option 2: Build Docker Image Locally
### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
### Build the Container
- Before building the container, ensure the project directory is organized as follows:
  t5-onnx-summarizer/
  │
  ├── Dockerfile
  ├── requirements.txt
  ├── infer.py
  ├── README.md
  │
  └── models/
    └── t5_small_onnx_quantized)/
        ├── encoder_model.onnx
        ├── decoder_model.onnx
        ├── decoder_with_past_model.onnx
        ├── config.json
        ├── tokenizer_config.json
        ├── tokenizer.json / spiece.model
        └── special_tokens_map.json
    └── t5_small_onnx]/
        ├── encoder_model.onnx
        ├── decoder_model.onnx
        ├── decoder_with_past_model.onnx
        ├── config.json
        ├── tokenizer_config.json
        ├── tokenizer.json / spiece.model
        └── special_tokens_map.json
  [t5_small_onnx and t5_small_onnx_quantized](https://drive.google.com/drive/folders/1t6bxuPiEnrbfll-Zz1PbXbqTQQ1CEFgD?usp=sharing) can  be found here.


Navigate to the project directory and run:
```bash
docker build -t t5-onnx-summarizer .
```
This process installs dependencies and packages the quantized ONNX model into the container.
## Method 1 — Summarize a Text File (Recommended)
Place the text file in your current directory and mount it into the container.
To run the container successfully, ensure that the file:

```
summarize_article.txt
```

is located in your **current working directory** before executing the Docker command.

This requirement applies to **Windows, macOS, and Linux**.

The Docker command mounts your current directory into the container, allowing the inference script to access the file.


### Windows (PowerShell)
``` powershell
docker run --rm `
-v "${PWD}:/data" `
gaoshuaige/t5-onnx-summarizer `
--file /data/summarize_article.txt
```
### macOS / Linux
```bash
docker run --rm \
-v "$(pwd)":/data \
gaoshuaige/t5-onnx-summarizer \
--file /data/summarize_article.txt
```
## Method 2 — Direct Text Input
```bash
docker run --rm gaoshuaige/t5-onnx-summarizer \
--text "Paste any technical paragraph here..."
```