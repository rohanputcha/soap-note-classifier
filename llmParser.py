import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)
    
image = Image.open("./pdf_images/page_1.png").convert("RGB")
messages = [
    {"role": "user", "content": [
        {"type": "image"},
        {"type": "text", "text": "Describe this image in two sentences"}
    ]}
]

input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(
    image,
    input_text,
    return_tensors="pt"
).to(model.device)

# print(inputs['input_ids'])

output = model.generate(**inputs, max_new_tokens=512)
print(processor.decode(output[0]))


