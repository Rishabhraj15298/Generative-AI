import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = "models/embedding-001"

text = "Sun rises in the east"

response = genai.embed_content(
    model,
    content = text,
)

embedding_vector = response["embedding"]

print("Length of embeddig:" , len(embedding_vector))
print("First 10 numbers : " , embedding_vector[:10])


# -------------------------------------------------------------------------------------------

# OUTPUT

# Length of embeddig: 768
# First 10 numbers :  [0.019840963, 0.008412288, -0.03634813, -0.027246889, 0.018013444,
#  0.0084295, 0.029299857, 0.033642586, -0.004409945, 0.011957156]