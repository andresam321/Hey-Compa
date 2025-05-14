from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch


MODEL_NAME = "naver-clova-ix/donut-base-finetuned-docvqa"
processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

def extract_with_donut(image_path, question="What is the total amount due?"):
    image = Image.open(image_path).convert("RGB")
    task_prompt = f"<s_docvqa><question>{question}</question><answer>"

    inputs = processor(image, task_prompt=task_prompt, return_tensors="pt")
    pixel_values = inputs.pixel_values
    decoder_input_ids = inputs.decoder_input_ids

    with torch.no_grad():
        outputs = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=512
        )

    result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return result.strip()
