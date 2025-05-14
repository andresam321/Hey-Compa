from transformers import DonutProcessor, VisionEncoderDecoderModel

print("📦 Downloading DonutProcessor...")
DonutProcessor.from_pretrained("naver-clova-ix/donut-base")

print("📦 Downloading DonutModel...")
VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")

print("✅ Donut downloaded and cached!")
