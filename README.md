# Health Chatbot: Chatbot berbasis Retrieval Augmented Generation (RAG) diintegrasikan Dengan Intent Classification

## Domain Proyek
Chatbot berbasis RAG (_Retrieval Agumented Generation_) ini dirancang untuk memberikan informasi terkai tiga topik utama: obat, menstruasi, dan alergi. Chatbot ini mengintegrasikan klasifikasi intent untuk memahami maksud pengguna dan kemudian melakukan pencarian informasi relevan berdasarkan topik yang diajukan, sebelum akhirnya menghasilkan jawaban menggunakan model generatif seperti GPT. Dengan kemampuan ini, chatbot dapat secara akurat menjawab pertanyaan yang berkaitan dengan ketiga topik tersebut.



## Business Understanding
### Problem Statements
- Bagaimana chatbot dapat secara efektif mengklasifikasikan maksud atau intent dari prompt pengguna?
- Bagaimana chatbot dapat memberikan respons terhadap pertanyaan terkait ketiga topik atau intent tersebut?
- Bagaimana cara mengintegrasikan sistem pencarian berbasis RAG dengan klasifikasi intent untuk meningkatkan kualitas respons?
### Goals
Tujuan proyek ini adalah untuk meningkatkan akurasi dalam menjawab pertanyaan terkait kesehatan, khususnya pada informasi medis mengenai obat-obatan, masalah menstruasi, dan alergi, dengan menggunakan teknik pemodean bahasa berbasis AI. Informasi yang digunakan oleh chatbot diambil dari sumber terpercaya yang dikumpulkan dari sebuah website kesehatan yang menyediakan layanan tanya jawab seputar topik tersebut.

### Solution Statements
Untuk mencapai tujuan diatas, maka dilakukan pencarian dataset yang terpercaya dan dapat divalidasi. Data ini akan digunakan sebagai basis pengetahuan untuk chatbot dan data untuk proses pelatihan model pada tugas _intent classification_.

Adapun model yang digunakan adalah untuk tugas _intent classification_ dipilih model IndoBERT [[1]](https://huggingface.co/indobenchmark/indobert-base-p1). Model tersebut di _fine-tuning_ menggunakan dataset yang didapatkan dari hasil crawling yang terdiri dari lebih dari 14000 baris data dengan 2 features yaitu 'intent' dan 'pertanyaan'. Kemudian untuk proses RAG nya digunakan ChromaDB sebagai penyimpanan basis pengetahuan chatbot dan GPT-3.5-Turbo sebagai model generatifnya.

## Data Understanding
Data yang digunakan dalam proyek ini adalah dataset yang terdiri dari lebih dar 14.000 baris data. Data tersebut didapatkan secara manual dengan melakukan teknik crawling pada sebuah website layanan kesehatan di Indonesia.

Preprocessing data dilakukan terhadap dataset tersebut untuk memastikan data yang dimasukkan ke model ataupun sebagai basis pengetahuan chatbot benar-benar siap pakai. Tahap pertama dilakukan proses transformasi teks menjadi _lower case_. Hal ini dilakukan untuk memastikan konsistensi data. Kemudian diikuti tahap penghapusan tanda baca serta karakter yang tidak dibutuhkan. Beberapa baris hasil crawling memiliki nilai null (_missing value_) di beberapa kolom sehingga perlu dihapus. Selain itu ditemukan juga beberapa data yang duplikat. Hal ini mungkin karena proses crawling dilakukan secara bertahap yang mengakibatkan duplikasi data.

Dataset yang telah selesai _preprocessing_ selanjutnya dipecah menjadi 2 dataset. Dataset pertama digunakan dalam proses _fine-tuning_ IndoBERT untuk tugas intent classification. Pada dataset yang pertama ini hanya digunakan 2 kolom saja yaitu kolom "intent" dan kolom "pertanyaan". Sedangkan dataset kedua digunakan sebagai basis pengetahuan chatbot. Sama seperti dataset pertama, dataset kedua juga hanya berisi 2 kolom saja yaitu "intent" dan "answer".


## Data Preparation
Pada proses ini hanya dilakukan terhadap dataset yang pertama yaitu untuk tugas _intent-classification_. Prosesnya juga tidak banyak yaitu hanya mengubah label saja. Label pada dataset yang pertama adalah kolom 'intent'. Terdapat 3 nilai dari kolom tersebut yaitu alergi, obat dan menstruasi. Untuk pelabelannya sendiri sebagai berikut:
- label 0 untuk data yang memiliki nilai 'intent' alergi
- label 1 untuk data yang memiliki nilai 'intent' obat
- label 2 untuk data yang memiliki nilai 'intent' menstruasi.

## Modelling
Seperti yang telah dijelaskan ada 2 tahapan dalam proyek ini yaitu _intent classification_ dan RAG.
### Intent Classification
Pada tugas ini, digunakan model IndoBERT[[1]](https://huggingface.co/indobenchmark/indobert-base-p1). Model tersebut di _fine-tuning_ menggunakan dataset yang pertama. _Fine-tuning_ dilakukan dengan cara melatih lapisan terakhir IndoBERT untuk menyesuaikan model dengan tugas spesifik, dalam hal ini _intent classification_. _Fine-tuning_ dilakukan dengan mengganti lapisan klasifikasi pada IndoBERT untuk melakukan prediksi terhdap tigas kelas intent yaitu obat, menstruasi dan alergi. Proses _fine-tuning_ ini dilakukan dengan menggunakan optimasi AdamW dan fungsi loss yang sesuai.

### Retrieval Augmented Generation (RAG)
Secara garis besar, RAG juga terbagi menjadi 2 proses yaitu proses retrieval dan generation. RAG digunakan untuk meningkatkan kemampuan chatbot dalam memberikan jawaban yang tidak hanya berbasis pada model prediktif, tetapi juga menggunakan _retrieved information_ dari basis pengetahuan yang relevan.

Proses RAG ini diawali dengan proses mengubah basis pengetahuan chatbot menjadi vektor yang nantinya akan dimasukkan kedalam database vektor. Pada proses ini embedding dilakukan menggunakan model dari SentenceTransformers yaitu ```all-MiniLM-L6-v2``` [[2]](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). Sedangkan vektor database yang digunakan adalah ChromaDB. Setelah itu, proses generatif dilakukan menggunakan GPT-3.5-Turbo (atau yang lain). Seluruh proses RAG ini dilakukan dengan bantuan library LangChain.


### Integrasi Intent Classification dan RAG
Pada akhirnya, kedua tugas tersebut akan digabungkan sehingga menjadi chatbot yang utuh. Adapun alur dari sistem yang dibangun adalah:
1. Sistem menerima prompt dari user
2. Prompt akan diteruskan ke model IndoBERT yang telah di _fine-tuning_ untuk diklasifikasikan intentnya
3. Setelah itu dilakukan pencarian informasi yang relevan berdasarkan intent dan prompt user tersebut
4. Setelah informasi didapatkan maka dikirim ke GPT-3.5-Turbo untuk di generate responsnya.



## Evaluation
Proses evaluasi pada proyek ini menggunakan 2 teknik yaitu evaluasi secara kuantitatif dan kualitatif. Evaluasi kuantitatif dilakukan pada tugas _intent-classification_ menggunakan metrik evaluasi _accuracy, precision, recall,_ dan _f1-score_. Adapun hasil dari tugas _intent-classification_ sebagai berikut:

- Accuracy: 94%
- Recall: 94%
- Precision: 94%
- F1-score: 94%

Sedangkan proses evaluasi pada proses RAG hanya dilakukan evaluasi kualitatif. Hasil evaluasi menunjukkan **80% pertanyaan yang diajukan berhasil dijawab dengan baik**. Walaupun begitu, masih ada pertanyaan yang belum bisa dijawab. Hal ini dikarekanakan beragamnya basis pengetahuan sehingga menyulitkan model untuk menghitung kedekatan (_similarity_) terhadap prompt. Selain itu, perbedaan panjang prompt dengan basis pengetahuan juga menjadi faktor penyebab. Dengan rata-rata jumlah kata setiap baris pada basis pengetahuan adalah 500-700 kata. Selain itu, ada beberapa informasi yang tidak relevan masih ikut masuk kedalam basis pengetahuan seperti pertanyaan lanjutan dari pengguna.

## Recommendation
Rekomendasi untuk proyek serupa dan menggunakan dataset yang sama untuk kedepan adalah sebagai berikut
- Lakukan pengawasan terhadap proses crawling sehingga yang masuk ke dataset betul-betul benar dan relevan
- Proses preprocessing lebih ditingkatkan lagi seperti dicek satu per satu apakah ada informasi yang tidak relevan
- Lakukan perhitungan metrik evaluasi untuk proses RAG menggunakan BLEU, ROUGE-1, ROUGE-2, dan matrik lainnya.


## Kebutuhan Lain
- Model IndoBERT yang sudah di _fine-tuning_ dapat diakses pada link berikut: [[KLIK DISINI]](https://huggingface.co/iqbalpurba26/IndoBERT_intent_classification)
- Dataset tidak dipublish secara umum. Untuk kebutuhan kolaborasi dapat mengubungi melalui LinkedIn: [[KLIK DISINI]](https://www.linkedin.com/in/m-iqbal-purba)