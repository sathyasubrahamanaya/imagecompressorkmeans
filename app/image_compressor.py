import cv2
import numpy as np

class FastImageCompressor:
    def __init__(self, target_size=0.25, K=16, max_iter=50, tol=1e-3):
        """
        Args:
            target_size (float): Resize factor (0.25 = 25% of original size)
            K (int): Number of clusters (colors)
            max_iter (int): Maximum K-means iterations
            tol (float): Convergence tolerance
        """
        self.target_size = target_size
        self.K = K
        self.max_iter = max_iter
        self.tol = tol

    def compress(self, input_path, output_path):
        # Load and resize image
        img = cv2.imread(input_path)
        h, w = img.shape[:2]
        new_h, new_w = int(h * self.target_size), int(w * self.target_size)
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Prepare data for K-means
        Z = resized.reshape((-1, 3)).astype(np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                   self.max_iter, self.tol)

        # K-means clustering
        _, labels, centers = cv2.kmeans(
            Z, self.K, None, criteria, 10, cv2.KMEANS_PP_CENTERS
        )

        # Reconstruct compressed image
        compressed = centers[labels.flatten()].reshape(resized.shape).astype(np.uint8)

        # Save as JPEG with optimized quality
        cv2.imwrite(output_path, compressed, [cv2.IMWRITE_JPEG_QUALITY, 80])

# Usage example
#compressor = FastImageCompressor(target_size=0.25, K=100, max_iter=4)
#compressor.compress("me.jpg", "compressed.jpg")