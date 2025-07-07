# Emotion Tag for Videos

Bu proje, videolardan yüzleri algılayıp kullanıcı etiketleriyle (mutlu, üzgün vb.) birlikte CSV formatında saklamayı, videonun sesini yazıya dökmeyi ve yazıların kelime analizini yaparak WordCloud oluşturmaya yarar.

## Alt Modüller

### 1. `label_tool/csv-label.py`
- Videodan yüz algılar.
- Her yüz için kullanıcıdan duygu etiketi alır.
- Etiketleri CSV'ye yazar.
- `frame_skip` ve `resize_factor` gibi ayarlanabilir parametreler içerir.

### 2. `audio_transcribe/voice_and_text.py`
- Videodan ses çıkarır.
- Whisper ile Türkçe konuşmayı yazıya döker.
- `.docx` olarak kaydeder.

### 3. `word_analysis/word_analyze.py`
- `.docx` metinleri tarar.
- Türkçe özel stopword'ler ile temizleme yapar.
- İlk 50 kelimeyi analiz eder ve WordCloud üretir.

## Dosya Yerleşimi
- Etiketli yüz fotoğrafları `sample_outputs/faces/`
- Transkript metinleri `sample_outputs/transcriptions/`
- Ses dosyaları `sample_outputs/audio/`
- Wordcloud görselleri `sample_outputs/wordclouds/`

## Çalıştırmak İçin
```bash
pip install -r requirements.txt
python label_tool/csv-label-rev5.py
python audio_transcribe/voice_and_text.py
python word_analysis/word_analyze.py
```

> Not: Scriptler içinde geçen dosya yolları bilgisayara uygun şekilde güncellenmelidir.

## Kullanım Amacı
- Etiketli veri toplamak (ML için uygun veri kümesi oluşturma).
- Kişiselleştirilmiş veri tabanları oluşturma.
- Otomatik transkripsiyon ve duygu analizi için temel hazırlık.
- Görsel metin analiziyle özet çıkarma.
