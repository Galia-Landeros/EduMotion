import json
import os

def main():
    path = os.path.join("data", "colors_sessions.json")
    if not os.path.exists(path):
        print("No hay sesiones registradas todavía.")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("Archivo vacío.")
        return

    total_sessions = len(data)
    avg_acc = sum(s["accuracy"] for s in data) / total_sessions
    avg_score = sum(s["score"] for s in data) / total_sessions

    print("=== Resumen EduMotion - Colores ===")
    print(f"Sesiones totales: {total_sessions}")
    print(f"Puntaje promedio: {avg_score:.2f}")
    print(f"Precisión promedio: {avg_acc*100:.1f}%")
    print()
    print("Últimas 5 sesiones:")
    for s in data[-5:]:
        print(f"- {s['timestamp']} | {s['username']} | "
              f"Score: {s['score']} / {s['attempts']} "
              f"({s['accuracy']*100:.1f}%)")

if __name__ == "__main__":
    main()
