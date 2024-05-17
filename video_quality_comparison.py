import argparse
import time
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_metrics(video1080_path, video4k_path):
    logging.info(f"Calculating metrics for videos {video1080_path} (1080p) and {video4k_path} (4K)")

    cap1080 = cv2.VideoCapture(str(video1080_path))
    cap4k = cv2.VideoCapture(str(video4k_path))

    if not cap1080.isOpened():
        logging.error(f"Could not open 1080p video file: {video1080_path}")
        return None, None

    if not cap4k.isOpened():
        logging.error(f"Could not open 4K video file: {video4k_path}")
        return None, None

    frame_count = int(cap1080.get(cv2.CAP_PROP_FRAME_COUNT))
    chunk_size = 100

    avg_psnr = 0
    avg_ssim = 0

    for i in tqdm(range(0, frame_count, chunk_size), desc="Processing frames"):
        psnr_values = []
        ssim_values = []

        for _ in range(chunk_size):
            ret1080, frame1080 = cap1080.read()
            ret4k, frame4k = cap4k.read()

            if not ret1080 or not ret4k:
                break

            # Resize the 4K frame to 1080p for comparison
            frame4k_resized = cv2.resize(frame4k, (frame1080.shape[1], frame1080.shape[0]))

            # Convert frames to grayscale
            gray1080 = cv2.cvtColor(frame1080, cv2.COLOR_BGR2GRAY)
            gray4k = cv2.cvtColor(frame4k_resized, cv2.COLOR_BGR2GRAY)

            # Calculate PSNR
            psnr_value = psnr(gray1080, gray4k)
            psnr_values.append(psnr_value)

            # Calculate SSIM
            ssim_value, _ = ssim(gray1080, gray4k, full=True)
            ssim_values.append(ssim_value)

        avg_psnr += np.mean(psnr_values)
        avg_ssim += np.mean(ssim_values)

    avg_psnr /= frame_count / chunk_size
    avg_ssim /= frame_count / chunk_size

    cap1080.release()
    cap4k.release()

    return avg_psnr, avg_ssim

def interpret_metrics(avg_psnr, avg_ssim):
    # Interpret PSNR
    if avg_psnr > 40:
        psnr_quality = "High quality, almost indistinguishable from the original."
    elif 30 < avg_psnr <= 40:
        psnr_quality = "Good quality, minor differences may be noticeable."
    elif 20 < avg_psnr <= 30:
        psnr_quality = "Acceptable quality, noticeable differences."
    else:
        psnr_quality = "Poor quality, significant degradation."

    # Interpret SSIM
    if avg_ssim > 0.95:
        ssim_quality = "High quality, minimal degradation."
    elif 0.90 < avg_ssim <= 0.95:
        ssim_quality = "Good quality, low degradation."
    elif 0.80 < avg_ssim <= 0.90:
        ssim_quality = "Moderate quality, noticeable degradation."
    else:
        ssim_quality = "Poor quality, significant degradation."

    return psnr_quality, ssim_quality

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate and interpret PSNR and SSIM metrics for two videos.')
    parser.add_argument('video1080_path', type=str, help='Path to the 1080p video file.')
    parser.add_argument('video4k_path', type=str, help='Path to the 4K video file.')
    return parser.parse_args()

args = parse_args()

video1080_path = Path(args.video1080_path)
assert video1080_path.exists(), f"1080p video file not found: {video1080_path}"
video4k_path = Path(args.video4k_path)
assert video4k_path.exists(), f"4K video file not found: {video4k_path}"

start_time = time.time()

avg_psnr, avg_ssim = calculate_metrics(video1080_path, video4k_path)

end_time = time.time()
execution_time = end_time - start_time

if avg_psnr is not None and avg_ssim is not None:
    logging.info(f'Average PSNR: {avg_psnr}')
    logging.info(f'Average SSIM: {avg_ssim}')
    
    psnr_quality, ssim_quality = interpret_metrics(avg_psnr, avg_ssim)
    logging.info(f'PSNR Interpretation: {psnr_quality}')
    logging.info(f'SSIM Interpretation: {ssim_quality}')
    logging.info(f'Time of execution: {execution_time} seconds')
else:
    logging.error('Failed to calculate metrics')