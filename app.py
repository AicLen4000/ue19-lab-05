import sys
import requests

API_URL = "https://v2.jokeapi.dev/joke/Any"


def fetch_joke(timeout: int = 10) -> str:
    params = {"safe-mode": ""}
    response = requests.get(API_URL, params=params, timeout=timeout)
    response.raise_for_status()

    data = response.json()
    if data.get("error"):
        raise RuntimeError(data.get("message", "Erreur renvoyée par l'API."))

    if data.get("type") == "single":
        return data.get("joke", "Aucune blague trouvée.")
    if data.get("type") == "twopart":
        return f"{data.get('setup', '')}\n→ {data.get('delivery', '')}"

    raise ValueError(f"Type de blague non pris en charge : {data.get('type')}")


def main() -> int:
    try:
        print(fetch_joke())
        return 0
    except requests.exceptions.RequestException as exc:
        print(f"Erreur réseau / HTTP : {exc}", file=sys.stderr)
        return 1
    except (ValueError, RuntimeError) as exc:
        print(f"Erreur de traitement : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())