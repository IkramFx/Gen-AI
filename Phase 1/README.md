# Gen-AI Phase 1

Materi dan latihan Python untuk dasar Generative AI, meliputi Python Core, data structures, OOP, file handling, asynchronous programming, NumPy, dan pandas.

## 1. Prasyarat

- Windows 10/11
- Git
- Python 3.11 atau lebih baru
- VS Code (disarankan)

Cek instalasi:

```powershell
git --version
python --version
```

## 2. Download Repository

```powershell
git clone https://github.com/IkramFx/Gen-AI.git
cd Gen-AI
cd "Phase 1"
```

Buka folder ini di VS Code:

```powershell
code .
```

## 3. Buat Virtual Environment

Jalankan dari folder `Phase 1`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika PowerShell menolak aktivasi script, jalankan PowerShell sebagai user biasa:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Kemudian ulangi perintah aktivasi.

## 4. Konfigurasi API Key

Salin file contoh:

```powershell
Copy-Item .env.example .env
```

Buka `.env` dan isi API key yang diperlukan. Jangan upload `.env` ke GitHub.

Sebagian besar contoh di repository menggunakan mock data dan tidak memerlukan API key. File `.env` hanya diperlukan ketika memakai client API nyata.

## 5. Pilih Interpreter VS Code

1. Tekan `Ctrl+Shift+P`.
2. Pilih `Python: Select Interpreter`.
3. Pilih interpreter dari `.venv`.

Path Windows biasanya:

```text
.venv\Scripts\python.exe
```

## 6. Menjalankan Contoh

Gunakan terminal dari root folder `Gen-AI`. Karena beberapa nama file memiliki spasi, gunakan tanda kutip.

### Module 1

```powershell
python "Module 1\1_6 exception handling.py"
python "Module 1\1_7 exercises.py"
```

### Module 2

```powershell
python "Module 2\2_6 generators.py"
python "Module 2\2_7 exercises.py"
```

### Module 3

```powershell
python "Module 3\3_3 decorators.py"
python "Module 3\3_4 dataclasses.py"
python "Module 3\3_6 exercises.py"
python "Module 3\3_5 import recently.py"
```

### Module 4

```powershell
python "Module 4\4_1 working at files_txt.py"
python "Module 4\4_1 working at files_json.py"
python "Module 4\4_1 working at files_csv.py"
python "Module 4\4_2 simulating llm api call.py"
python "Module 4\4_2 async & await.py"
python "Module 4\4_3 environtment variable & secrets.py"
python "Module 4\4_4 exercises.py"
```

`4_2 async & await.py` dan beberapa latihan endpoint membutuhkan koneksi internet.

### Module 5

```powershell
python "Module 5\5_1 array & dtypes.py"
python "Module 5\5_1 shape,reshape,indexing.py"
python "Module 5\5_1 cosine similarity.py"
python "Module 5\5_2 creating & inspecting dataframes.py"
python "Module 5\5_2 filtering & selection.py"
python "Module 5\5_2 cleaning & transforming.py"
python "Module 5\5_2 groupby & aggregation.py"
python "Module 5\5_3 mini projects.py"
```

## 7. Menjalankan File Python Lain

Format umum:

```powershell
python "Module X\nama file.py"
```

Untuk mengecek sintaks tanpa menjalankan program:

```powershell
python -m py_compile "Module X\nama file.py"
```

## 8. File Hasil Program

Beberapa contoh membuat file hasil seperti `results.json`, `eval.csv`, `conversation.json`, dan `eval_results.csv`. File tersebut dibuat otomatis ketika program dijalankan.

## 9. Troubleshooting

### `ModuleNotFoundError`

Pastikan virtual environment aktif, lalu install dependency:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### `python` tidak ditemukan

Install Python dari python.org, aktifkan opsi `Add Python to PATH`, lalu buka terminal baru.

### Import package Module 3 gagal

Pastikan command dijalankan dari root repository `Gen-AI`, bukan dari folder `Module 3`.

### Program async gagal mengambil URL

Pastikan internet aktif. Beberapa endpoint publik dapat membatasi request atau sementara tidak tersedia.