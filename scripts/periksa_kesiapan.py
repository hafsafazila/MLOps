import importlib
import subprocess
import sys


def git(*args):
    hasil = subprocess.run(["git", *args], capture_output=True, text=True)
    return hasil.stdout.strip()


pemeriksaan = []

versi = sys.version_info[:2]
pemeriksaan.append(("Python 3.10.x aktif", versi == (3, 10), sys.version.split()[0]))

pemeriksaan.append(
    ("Lingkungan virtual aktif", sys.prefix != sys.base_prefix, sys.executable)
)

hilang = []
for nama in ["pandas", "numpy", "sklearn", "scipy", "yaml", "joblib"]:
    try:
        importlib.import_module(nama)
    except ImportError:
        hilang.append(nama)
pemeriksaan.append(
    ("Pustaka inti dapat diimpor", not hilang, ", ".join(hilang) or "semua ada")
)

nama_git = git("config", "user.name")
email_git = git("config", "user.email")
pemeriksaan.append(
    ("Git terkonfigurasi", bool(nama_git and email_git), f"{nama_git} <{email_git}>")
)

crlf = git("config", "core.autocrlf")
pemeriksaan.append(("Akhir baris dikonfigurasi", crlf in ("true", "input"), crlf))

remote = git("remote", "-v")
pemeriksaan.append(
    ("Remote origin dan upstream ada", "origin" in remote and "upstream" in remote, "")
)

lulus = 0
for judul, ok, rincian in pemeriksaan:
    lulus += ok
    print(f"[{'OK' if ok else 'GAGAL'}] {judul}  {rincian}")

print(f"\n{lulus}/{len(pemeriksaan)} lulus")
sys.exit(0 if lulus == len(pemeriksaan) else 1)
