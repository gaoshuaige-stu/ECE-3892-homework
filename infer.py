# infer.py
import argparse
from pathlib import Path

from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM

def load_text(args):
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    raise ValueError("Provide --text or --file")

def main():
    parser = argparse.ArgumentParser(description="ONNX T5 summarizer (CPU)")
    parser.add_argument("--model_dir", default="models/t5_small_onnx", help="Path to ONNX model folder")
    parser.add_argument("--text", type=str, default=None, help="Text to summarize")
    parser.add_argument("--file", type=str, default=None, help="Path to a text file to summarize")
    parser.add_argument("--max_input_length", type=int, default=512)
    parser.add_argument("--max_length", type=int, default=120)
    parser.add_argument("--min_length", type=int, default=40)
    parser.add_argument("--num_beams", type=int, default=4)
    args = parser.parse_args()

    raw = load_text(args)
    # T5 expects task prefix
    input_text = "summarize: " + raw.strip()

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = ORTModelForSeq2SeqLM.from_pretrained(args.model_dir)

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=args.max_input_length,
        truncation=True,
    )

    summary_ids = model.generate(
        **inputs,
        max_length=args.max_length,
        min_length=args.min_length,
        num_beams=args.num_beams,
        no_repeat_ngram_size=3,
        early_stopping=True,
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print(summary)

if __name__ == "__main__":
    main()
