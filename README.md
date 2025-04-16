# Acil Durum Asistanı

Bu proje, acil durum mesajlarını analiz eden ve aciliyet seviyesini belirleyen bir API servisidir.

## Özellikler

- Acil durum mesajlarını analiz etme
- 1-5 arası aciliyet puanı belirleme
- Detaylı gerekçe ve öneriler sunma
- Gemini AI entegrasyonu

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyasını düzenleyin ve Google Gemini API anahtarınızı ekleyin:
```
GOOGLE_API_KEY=your_api_key_here
```

3. Uygulamayı başlatın:
```bash
python main.py
```

## Kullanım

API'ye POST isteği göndererek acil durum mesajlarını analiz edebilirsiniz:

```bash
curl -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d '{"message": "Acil durum mesajınız"}'
```

## Yanıt Formatı

API, aşağıdaki formatta bir JSON yanıtı döndürür:

```json
{
    "urgency": 3,
    "rationale": "Açıklama",
    "suggestions": "Öneriler"
}
```

## Lisans

MIT 