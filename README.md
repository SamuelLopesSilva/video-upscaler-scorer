# Overview

This is a initial scorer for a video upscaler.

## Peak Signal-to-Noise Ratio (PSNR)

**Guide to Interpretation::**

**Higher PSNR values** indicate better quality. Typical PSNR values for lossy image and video compression are between 30 and 50 dB for 8-bit data, with higher values indicating better quality.

* **PSNR > 40 dB**: High quality, almost indistinguishable from the original.
* **30 dB < PSNR < 40 dB**: Good quality, minor differences may be noticeable.
* **20 dB < PSNR < 30 dB**: Acceptable quality, noticeable differences.
* **PSNR < 20 dB**: Poor quality, significant degradation.

## Structural Similarity Index (SSIM)

**Guide to Interpretation:**

**SSIM values range from -1 to 1**, where 1 indicates perfect similarity, 0 indicates no similarity, and -1 indicates perfect anti-correlation.

* **SSIM > 0.95**: High quality, minimal degradation.
* **0.90 < SSIM < 0.95**: Good quality, low degradation.
* **0.80 < SSIM < 0.90**: Moderate quality, noticeable degradation.
* **SSIM < 0.80**: Poor quality, significant degradation.

## Usage

```bash
python video_quality_comparison.py video_1080.mp4 video_4k.mp4
```
