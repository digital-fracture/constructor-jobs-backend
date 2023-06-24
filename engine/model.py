def predict(text: str) -> dict[str, str]:
    return {
        "requirements": text[:len(text) // 3],
        "conditions": text[len(text) // 3:len(text) // 3 * 2],
        "notes": text[len(text) // 3 * 2:],
    }
