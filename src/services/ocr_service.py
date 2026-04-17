from __future__ import annotations

from pathlib import Path

import cv2
import pytesseract
from PIL import Image


class TextExtractor:

    def __init__(
        self,
        lang: str = "eng",
        psm: int = 6,
        tesseract_cmd: str | Path | None = None,
    ) -> None:
        self.lang = lang
        self.psm = psm
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = str(tesseract_cmd)

    def _preprocess(self, image_path: Path) -> Image.Image:
        img = cv2.imread(str(image_path))
        if img is None:
            raise FileNotFoundError(f"Não foi possível abrir a imagem: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if min(gray.shape) < 1600:
            gray = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        return Image.fromarray(gray)

    def extract(self, image_path: str | Path) -> str:
        image = self._preprocess(Path(image_path))
        config = f"--oem 3 --psm {self.psm} -c preserve_interword_spaces=1"
        return pytesseract.image_to_string(image, lang=self.lang, config=config)
