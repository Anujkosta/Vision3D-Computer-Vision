from pathlib import Path
import cv2

def load_image(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")
    img = cv2.imread(str(p))
    if img is None:
        raise ValueError(f"Unable to read image: {p}")
    return img

def grayscale(img): return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
def gaussian_blur(img, ksize=(5,5)): return cv2.GaussianBlur(img, ksize, 0)
def median_blur(img, ksize=5): return cv2.medianBlur(img, ksize)
def histogram_equalization(gray): return cv2.equalizeHist(gray)
def canny_edges(gray, low=100, high=200): return cv2.Canny(gray, low, high)

def save(path, image):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)

def run_preprocessing(input_path, output_dir="results/preprocessing"):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    img = load_image(input_path); gray = grayscale(img)
    save(out/"01_grayscale.png", gray)
    save(out/"02_gaussian_blur.png", gaussian_blur(gray))
    save(out/"03_median_blur.png", median_blur(gray))
    save(out/"04_histogram_equalized.png", histogram_equalization(gray))
    save(out/"05_canny_edges.png", canny_edges(gray))
    print(f"Preprocessing completed. Results: {out.resolve()}")
