from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import BartTokenizer, BartForConditionalGeneration

def translate(sentence, **argv):
    inputs = tokenizer(sentence, return_tensors="pt")
    generated_ids = generator.generate(inputs["input_ids"], **argv)
    decoded = tokenizer.decode(generated_ids[0], skip_special_tokens=True).replace(" ", "")
    return decoded

path = "KomeijiForce/bart-base-emojilm"
tokenizer = BartTokenizer.from_pretrained(path)
generator = BartForConditionalGeneration.from_pretrained(path)

app = FastAPI()

origins = [
    "http://localhost:56409",  # Your Flutter app's origin
    "http://localhost:8888", # The local host of the API
    "http://localhost:61785",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextModel(BaseModel):
    text: str


@app.post("/translate")
def translate_text(body: TextModel):
    # take input text and return it translated into emoji
    decoded = translate(body.text, num_beams=4, do_sample=True, max_length=100)
    return {"translated_text": decoded}