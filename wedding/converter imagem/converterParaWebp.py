from pathlib import Path
from PIL import Image

# ====== CONFIG ======
QUALITY = 82                 # 75–85 é o ideal para web
METHOD = 6                   # 0–6 (6 = melhor compressão)
LOSSLESS_FOR_PNG = False     # False = arquivos menores
DELETE_ORIGINAL = False      # True = apaga png/jpg após converter
OVERWRITE = False            # True = sobrescreve webp existente
# ====================

VALID_EXTS = {".png", ".jpg", ".jpeg"}

# pasta onde está este script
BASE_DIR = Path(__file__).resolve().parent


def convert_image(src: Path) -> bool:
    dst = src.with_suffix(".webp")

    if dst.exists() and not OVERWRITE:
        return False

    try:
        with Image.open(src) as im:
            im.load()

            # normaliza modo
            if im.mode in ("P", "LA"):
                im = im.convert("RGBA")
            elif im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")

            save_args = {
                "format": "WEBP",
                "quality": QUALITY,
                "method": METHOD,
                "optimize": True
            }

            if src.suffix.lower() == ".png":
                save_args["lossless"] = LOSSLESS_FOR_PNG
            else:
                if im.mode != "RGB":
                    im = im.convert("RGB")

            im.save(dst, **save_args)

        if DELETE_ORIGINAL:
            src.unlink(missing_ok=True)

        return True

    except Exception as e:
        print(f"[ERRO] {src.name} -> {e}")
        return False


def main():
    scanned = 0
    converted = 0

    for path in BASE_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() in VALID_EXTS:
            scanned += 1
            if convert_image(path):
                converted += 1
                print(f"[OK] {path.relative_to(BASE_DIR)}")

    print("\nResumo:")
    print(f"• arquivos encontrados: {scanned}")
    print(f"• convertidos: {converted}")
    print(f"• pasta base: {BASE_DIR}")


if __name__ == "__main__":
    main()
