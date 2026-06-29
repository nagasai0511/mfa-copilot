import os

from groq import Groq

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

MODEL = "llama-3.3-70b-versatile"


def generate(prompt):

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0.3,

        max_completion_tokens=3500,

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a Senior IBM Mainframe Migration "
                    "Architect specializing in IBM z/OS to "
                    "Micro Focus Enterprise Server migration."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ]
    )

    return response.choices[0].message.content
