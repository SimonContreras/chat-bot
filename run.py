from dotenv import load_dotenv

load_dotenv()
import os

u_oken = os.getenv("OPENAI_API_KEY")
u = User.parse_file(
    "/home/simon/dev/chat-poc/db/users/e4ee7459-fdbd-417d-97ff-6ce2feb84612-a-test-email@test-email.com.json"
)
a = OpenAiApi(u_oken, u)
chat = "3a51470a-4376-424c-a875-1d93d031a93b"
conte = "Que es el principio de inceridumbre, me puedes dar un ejemplo de la vida cotidiana?"
a.resolve_api_call(chat, conte)
