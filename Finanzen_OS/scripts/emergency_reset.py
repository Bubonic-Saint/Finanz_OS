import os
import psutil  # Falls nicht installiert: pip install psutil
import time


def reset_system():
    print("Säubere System...")
    current_pid = os.getpid()

    # 1. Alle anderen Python-Prozesse beenden
    for proc in psutil.process_iter(['pid', 'name']):
        if 'python' in proc.info['name'].lower() and proc.info['pid'] != current_pid:
            try:
                proc.terminate()
                print(f"Prozess {proc.info['pid']} beendet.")
            except:
                pass

    # 2. Kurze Pause für Windows
    time.sleep(1)

    # 3. Teste, ob Dateien schreibbar sind
    paths = [
        r"C:\Users\kevin\Git\Finanzen_OS\data\input\bank_upload.csv",
        r"C:\Users\kevin\Git\Finanzen_OS\data\output\ready_for_excel.csv"
    ]

    for path in paths:
        if os.path.exists(path):
            try:
                os.rename(path, path)  # Testet, ob Datei gesperrt ist
                print(f"Datei frei: {os.path.basename(path)}")
            except OSError:
                print(f"WARNUNG: {os.path.basename(path)} wird noch von einem Programm (Excel?) blockiert.")


if __name__ == "__main__":
    reset_system()