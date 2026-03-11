import os
import psutil
import time


def reset_system():
    # 1. Verzeichnisse relativ ermitteln
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    paths = [
        os.path.join(base_dir, "data", "input", "bank_upload.csv"),
        os.path.join(base_dir, "data", "output", "ready_for_excel.csv")
    ]

    print("--- System-Check & Bereinigung ---")
    current_pid = os.getpid()

    # 2. Gezieltes Beenden (Optional, falls Dateien gesperrt sind)
    # Anstatt alle Python-Prozesse zu killen, prüfen wir erst, ob Dateien gesperrt sind
    for path in paths:
        if os.path.exists(path):
            try:
                # Test: Umbenennen ist der beste Weg, um Sperren unter Windows zu prüfen
                os.rename(path, path)
                print(f"Check: {os.path.basename(path)} ist frei verfügbar.")
            except OSError:
                print(f"INFO: {os.path.basename(path)} ist gesperrt. Suche nach blockierenden Prozessen...")

                # Nur wenn gesperrt, versuchen wir Prozesse zu finden (vorsichtiger Ansatz)
                for proc in psutil.process_iter(['pid', 'name']):
                    if 'python' in proc.info['name'].lower() and proc.info['pid'] != current_pid:
                        try:
                            proc.terminate()
                            print(f"Gesperrter Python-Prozess {proc.info['pid']} wurde beendet.")
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                time.sleep(1)

    print("Bereinigung abgeschlossen.\n")


if __name__ == "__main__":
    reset_system()