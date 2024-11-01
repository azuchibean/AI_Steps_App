# for LLM model import, this is an example and not the actual usage

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class TextGenerationModel:
    def __init__(self, model_name="gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_text(self, prompt: str, max_length: int = 50) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs["input_ids"], max_length=max_length, num_return_sequences=1)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text

# Initialize the model globally to avoid reloading it with every request
text_generation_model = TextGenerationModel()

if __name__ == "__main__":
    prompt = input("Enter a prompt: ")
    max_length = int(input("Enter max length for the generated text: "))
    output = text_generation_model.generate_text(prompt, max_length)
    print("Generated Text:", output)