# Diskrit Lab

Diskrit Lab adalah prototipe web berbasis Python dengan antarmuka chat. Agent lokal mengenali sejumlah pola pertanyaan Bahasa Indonesia, lalu meneruskannya ke solver deterministik; tidak ada LLM atau API eksternal.

## Cakupan MVP

- Logika proposisional: tabel kebenaran dan klasifikasi tautologi, kontradiksi, atau kontingensi. Operator yang didukung: `and`, `or`, `not`, dan `^` (XOR).
- Himpunan: gabungan, irisan, selisih, dan beda simetris; masukkan literal seperti `{1, 2, 3}`.
- Kombinatorika: permutasi dan kombinasi dengan syarat `0 ≤ r ≤ n`.
- Graf sederhana tak berarah: derajat simpul, jumlah sisi, komponen, dan keterhubungan. Sisi ditulis satu per baris seperti `A-B`.
- Relasi pada domain hingga: refleksif, simetris, antisimetris, transitif, dan ekuivalensi. Pasangan ditulis seperti `a,b`, satu per baris.

## Contoh pertanyaan di chat

```text
Tabel kebenaran p and not p
Operasi himpunan A={1,2}, B={2,3}
Berapa cara memilih 3 dari 8?
Analisis graf simpul: A, B, C sisi: A-B; B-C
Periksa relasi domain: a, b relasi: (a,a); (b,b); (a,b); (b,a)
```

Agent juga menerima variasi bahasa sederhana. Jika pola soal ambigu atau tidak termasuk cakupan di atas, agent akan meminta format yang didukung atau menjelaskan bahwa soal belum dikenali. Agent ini bukan model bahasa generatif dan tidak menyelesaikan pembuktian bebas.

## Menjalankan aplikasi

Gunakan Python 3.10 atau lebih baru. Pasang dependensi lalu jalankan:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Buka URL lokal yang ditampilkan Streamlit di browser.

## Menjalankan tes

```bash
python -m unittest -v
```

Ini bukan mesin yang memahami seluruh soal matematika diskrit. Soal berbahasa bebas, pembuktian umum, dan topik di luar cakupan belum didukung; keluaran hanya berlaku untuk format input dan operasi yang dijelaskan di atas.