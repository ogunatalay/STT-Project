# -*- coding: utf-8 -*-
"""STT PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e3ct3w_7muDpP8UkPCzIeHcfArCX8QWB
"""

!pip install transformers torchaudio

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import librosa

# Model ve işlemciyi yükleyin
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")

# Ses dosyasını yükleyin
audio_input, _ = librosa.load("/content/english_audio_16000hz.wav", sr=16000)

# Ses verisini işleyin
input_values = processor(audio_input, return_tensors="pt").input_values

# Modeli çalıştırın
with torch.no_grad():
    logits = model(input_values).logits

# En olası tahminleri al
predicted_ids = torch.argmax(logits, dim=-1)

# Metne dönüştürme
transcription = processor.decode(predicted_ids[0])
print("Tanınan Metin:", transcription)

import numpy as np
import re

# Sayıların yazılı karşılıklarını dönüştürmek için bir sözlük
number_to_words = {
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "10": "ten",
    "100": "one hundred",
    "1000": "one thousand"
}

def clean_text(text):
    # Sayıları yazılı karşılıklarıyla değiştirme
    for number, word in number_to_words.items():
        text = text.replace(number, word)

    # Küçük harfe çevir
    text = text.lower()

    # Noktalama işaretlerini kaldır
    text = re.sub(r'[^\w\s]', '', text)

    # Fazla boşlukları kaldır
    text = ' '.join(text.split())

    return text

def word_error_rate(reference, hypothesis):
    # Metinleri temizle
    reference = clean_text(reference).split()
    hypothesis = clean_text(hypothesis).split()

    # Substitutions, Insertions, Deletions hesaplamak
    substitution = sum([1 for ref, hyp in zip(reference, hypothesis) if ref != hyp])
    deletion = len(reference) - len(hypothesis)
    insertion = len(hypothesis) - len(reference)

    # Kelime hatası oranını hesapla
    wer = (substitution + deletion + insertion) / len(reference)
    return wer

# Gerçek ve tahmin edilen metinler
reference_text = "Hello, this is a test sentence to generate a 10-second MP3 file. It serves as an example for demonstrating how we can convert text into speech using Python and create an audio file that can be easily played and shared."
hypothesis_text = "HELLO THIS IS A TEST SENTENCE TO GENERATE A TEN SECOND M P THREE FILE IT SERVES AS AN EXAMPLE FOR DEMONSTRATING HOW WE CAN CONVERT TEXT INTO SPEECH USING PYTHEN AND CREATE AN AUDIOPHILE THAT CAN BE EASILY PLAYED AND SHARED"

# WER hesapla
wer = word_error_rate(reference_text, hypothesis_text)
print(f"Kelime Hatası Oranı (WER): {wer:.4f}")

# Gerçek etiketler (referans metin) ve tahmin edilen etiketler (hipotez metni)
reference_words = reference_text.split()
hypothesis_words = hypothesis_text.split()

# Doğru kelimeleri tespit etme
true_positives = sum([1 if word in hypothesis_words else 0 for word in reference_words])
false_positives = len(hypothesis_words) - true_positives
false_negatives = len(reference_words) - true_positives

# Precision, Recall, F1 hesaplama
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"Hassasiyet (Precision): {precision:.4f}")
print(f"Duyarlılık (Recall): {recall:.4f}")
print(f"F1 Skoru: {f1:.4f}")

import matplotlib.pyplot as plt

# Metrikler
metrics = ['Precision', 'Recall', 'F1 Score']
values = [0.7857, 0.8250, 0.8049]

# Grafik
plt.figure(figsize=(8,6))
plt.bar(metrics, values, color=['blue', 'green', 'orange'])

# Başlık ve etiketler
plt.title('Model Performans Metrikleri')
plt.xlabel('Metrikler')
plt.ylabel('Değerler')

# Grafik gösterimi
plt.ylim(0, 1)  # Y eksenini 0 ile 1 arasında sınırla
plt.show()

import time
import torch
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Ses dosyasını yükleyin
audio_input, _ = librosa.load("/content/english_audio_16000hz.wav", sr=16000)

# Model ve işlemciyi yükleyin
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")

# GPU'yu kontrol et
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Modeli belirtilen cihazda çalıştırmak için modelin cihazını ayarlıyoruz
model.to(device)

# Ses verisini işleyin
input_values = processor(audio_input, return_tensors="pt").input_values.to(device)

# Performans Testi - GPU üzerinde
start_time_gpu = time.time()

# Modeli çalıştırın (GPU)
with torch.no_grad():
    logits = model(input_values).logits

end_time_gpu = time.time()
gpu_time = end_time_gpu - start_time_gpu
print(f"GPU üzerinde işlem süresi: {gpu_time:.4f} saniye")

# Performans Testi - CPU üzerinde
start_time_cpu = time.time()

# Modeli çalıştırın (CPU)
model.to("cpu")  # Modeli CPU'ya taşıyoruz
input_values_cpu = input_values.to("cpu")

with torch.no_grad():
    logits_cpu = model(input_values_cpu).logits

end_time_cpu = time.time()
cpu_time = end_time_cpu - start_time_cpu
print(f"CPU üzerinde işlem süresi: {cpu_time:.4f} saniye")

# Performans karşılaştırması
speedup = cpu_time / gpu_time
print(f"GPU hız avantajı: {speedup:.2f}x")