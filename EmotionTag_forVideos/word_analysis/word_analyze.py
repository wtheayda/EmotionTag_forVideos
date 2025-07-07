import os
from docx import Document
from collections import Counter
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Stopwords ekle
nltk.download('stopwords')
stop_words = set(stopwords.words('turkish'))

# Ekstra Türkçe stopwords
extra_stopwords = {
    "bir", "böyle", "kadar", "falan", "hani", "bunu", "şey", "şeyi","şeye", "şeyler", "şeylere", "gerçekten", "an", "şuan", "şu an","anda", "kendini",
    "işte", "artık", "şekilde", "beni", "sadece", "kendi", "olarak", "bile", "var",
    "zaten", "tabii", "bunun", "hiçbir", "kendime", "yüzden", "kendim","kendimi", "öyle", "hala", "karar",
    "olan", "olduğu", "olduğun", "olduğum", "olduğunu", "şeyi", "şeyleri", "şöyle", "mesela",
    "gibi", "yani", "şunu", "böylece", "herhangi", "biraz", "göre", "mi", "mı", "ondan", "bundan",
    "mu", "mü", "değil", "daha", "çok", "yok", "hiç", "sanki", "ben", "benim", "bana", "sen","senin", "sana",
    "o", "onun", "ona", "biz", "bizim", "bize", "siz", "sizin", "size", "onlar", "onların", "onlara",
    "şu", "şunun", "şuna", "şunu", "şöyle", "şöyleki", "şöylece", "hatta", "orada", "burada", "oraya", "oradan", "buraya", "olması", "olması", "oldu", "olduğunu", "olacak", "olacaksa", "olursa", "olmadı", "olmadığını", "olmaz", "olmazsa",
}
stop_words.update(extra_stopwords)

# DOCX dosyalarını oku
def read_docx_files(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.docx'):
            doc = Document(os.path.join(folder_path, filename))
            full_text = ' '.join([para.text for para in doc.paragraphs])
            texts.append(full_text)
    return texts

# Kelime temizleme ve sayma
def clean_and_count_words(texts):
    all_words = []
    for text in texts:
        words = text.lower().split()
        words = [w.strip('.,!?()"\'') for w in words if w not in stop_words and w.isalpha()]
        all_words.extend(words)
    return Counter(all_words)

# Word cloud görselleştirme ve kaydetme
def visualize_wordcloud(counter, folder_path, max_words=50):
    most_common_words = dict(counter.most_common(max_words))
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=max_words,
        colormap='viridis',
        contour_width=1,
        contour_color='steelblue'
    ).generate_from_frequencies(most_common_words)

    # Yıl bilgisi
    folder_name = os.path.basename(folder_path)
    year = folder_name[:4] if folder_name[:4].isdigit() else "unknown"
    save_path = os.path.join(folder_path, f"wordcloud_{year}.png")

    # Görselleştir
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
   # plt.title(f"En Sık Geçen {max_words} Kelime - {year}", fontsize=16)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

    print(f"\n✅ Wordcloud görseli şuraya kaydedildi:\n{save_path}")

# Klasör yolu
folder_path = "sample_outputs/transcriptions"

# Akış
texts = read_docx_files(folder_path)
word_counts = clean_and_count_words(texts)
visualize_wordcloud(word_counts, folder_path, max_words=50)

# İlk 50 kelimeyi yazdır
print("\nEn sık geçen 50 kelime:")
for word, count in word_counts.most_common(50):
    print(f"{word}: {count}")
