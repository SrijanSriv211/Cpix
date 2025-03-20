from groq import Groq

class GROQ:
    def __init__(self, GroqAPI_path):
        with open(GroqAPI_path, "r", encoding="utf-8") as f:
            GROQ_API_KEY = str(f.read().strip())

        self.client = Groq(api_key = GROQ_API_KEY)

    def generate(self, text, model_name = "llama-3.3-70b-versatile"):
        text = "Human: " + text

        completion = self.client.chat.completions.create(
            messages = [
                {
                    "role": "system",
                    "content": "you are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model = model_name
        )

        return completion.choices[0].message.content
