import openai
import tools.credentials as credentials


def completion(information_relevant, prompt):

    prompt = f"""
    Anda adalah seorang dokter ahli spesialis dalam menajwab pertanyaan seputar obat, menstruasi, dan alergi. Anda diwajibkan untuk menjawab seluruh pertanyaan pasien dengan baik dan benar berdasarkan informasi yang diberikan.

    Informasi: 
    {information_relevant}

    Pertanyaan:
    {prompt}

    Jawabalah pertanyaan itu berdasarkan informasi yang diberikan saja. Ingat, kamu tidak boleh berhalusinasi dalam menjawab pertanyaan. Jika kamu tidak tahu atau pertanyaan tidak relevan dengan informasi yang diberikan maka jawab dengan "Mohon maaf. Saya tidak mengerti tentang pertanyaan anda, silahkan masukkan pertanyaan kembali dengan kalimat yang lebih sederhana".
    """

    response = openai.Completion.create(
        engine = credentials.DEPLOYMENT_CHAT,
        prompt=prompt,
        max_tokens=1000,
        temperature=0
    )

    return response['choices'][0]['text'].strip()
