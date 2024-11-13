from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

class LLMModel:
    def __init__(self):
        # Load a suitable T5 model; you can choose from 't5-small', 't5-base', 't5-large', or 'google/flan-t5-large'
        model_name = "t5-base"  # You can change this based on your compute capability
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

    def generate_text(self, prompt, task="general", max_length=512):
        # Prepend task-specific prefix if needed
        print(prompt)
        if task == "summarization":
            input_text = f"summarize: {prompt}"
        elif task == "qa":
            input_text = f"question: {prompt}"
        elif task == "review":
            input_text = f"generate a review: {prompt}"
        else:
            input_text = prompt

        inputs = self.tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)
        inputs = inputs.to(self.device)

        # Generate outputs
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=2
        )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text
