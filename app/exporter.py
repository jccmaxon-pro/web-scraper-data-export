from pathlib import Path
import pandas as pd


def export_to_excel(data: list[dict], filename: str) -> str:
    Path("output").mkdir(exist_ok=True)

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    return filename


def export_to_csv(data: list[dict], filename: str) -> str:
    Path("output").mkdir(exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    return filename