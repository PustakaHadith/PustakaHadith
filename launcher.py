#!/usr/bin/env python3
# Pelancar ringkas untuk PustakaHadith

import sys
import os
import subprocess


def main():
    print("PustakaHadith - Pelancar")
    print("=" * 40)

    # Semak versi Python
    print("Versi Python :", sys.version)

    # Semak folder semasa
    print("Folder semasa:", os.getcwd())

    # Jalankan aplikasi utama
    try:
        print("\nMenjalankan aplikasi PustakaHadith...")
        result = subprocess.run([sys.executable, "main.py"],
                                capture_output=True, text=True, check=True)
        print("Aplikasi selesai dengan jayanya")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Ralat semasa menjalankan aplikasi: {e}")
        if e.stdout:
            print("Keluaran:", e.stdout)
        if e.stderr:
            print("Ralat:", e.stderr)
        return 1
    except Exception as e:
        print(f"Ralat tidak dijangka: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
