import tiktoken 

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Sun rises in the east"
tokens = enc.encode(text)

print("Tokens :", tokens )

tokens = [30112, 67628, 306, 290, 23557]
decoded = enc.decode(tokens)

print("Decoded data :" , decoded)