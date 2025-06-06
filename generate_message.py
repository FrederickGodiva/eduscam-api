from openai import OpenAI
import  credentials as credentials

async def generate_scam_message():
    
    system_prompt = (
        """ 
    Anda adalah chatbot edukatif yang mensimulasikan percakapan scammer untuk mengajari pengguna tentang bahaya penipuan online. Buatlah pesan awal yang menyakinkan seolah-olah Anda adalah seorang scammer yang mencoba menipu korban dengan hadiah palsu atau urgensi tinggi. Kamu tidak perlu membuat template bahwa ini sebagai simulasi. Berikan saja langsung pesannya. Pesan yang kamu buat haruslah sesuai dengan kondisi di Indonesia seperti mata uang, dan lain-lain.
    """
    )

    client = OpenAI(
        api_key=credentials.API_KEY
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system","content": system_prompt}
        ]
    )

    return completion.choices[0].message.content