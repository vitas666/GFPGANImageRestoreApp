import cv2
import torch
import sys
import numpy as np
from PIL import Image
from gfpgan import GFPGANer
from torchvision.transforms import functional as F
try:
    from torchvision.transforms import functional_tensor
except ImportError:
    # If the module is missing (newer PyTorch), we create a fake one pointing to the new location
    sys.modules['torchvision.transforms.functional_tensor'] = F

class ImageRestorer:
    def __init__(self):
        # 1. Setup Device (Apple Silicon Acceleration)
        if torch.backends.mps.is_available():
            self.device = 'mps'
        else:
            self.device = 'cpu'
        
        print(f"AI Backend Initialized on: {self.device.upper()}")

        # 2. Initialize the GFPGAN Model
        # This will automatically download the weights (approx 300MB) 
        # to a local 'weights' folder the first time you run it.
        self.restorer = GFPGANer(
            model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
            upscale=2,              # Upscale the image 2x
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=None,      # Set to None for now to speed up testing
            device=self.device
        )

    def restore(self, pil_image):
        """
        Takes a PIL image (from Streamlit), fixes it, and returns a PIL image.
        """
        # --- Convert PIL (RGB) to OpenCV (BGR) ---
        # AI models usually work with BGR arrays (Blue-Green-Red)
        open_cv_image = np.array(pil_image) 
        # Convert RGB to BGR
        img_bgr = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # --- Run Inference (The Magic) ---
        # cropped_faces: individual faces found
        # restored_faces: the fixed faces
        # restored_img: the full final image
        _, _, restored_img_bgr = self.restorer.enhance(
            img_bgr, 
            has_aligned=False, 
            only_center_face=False, 
            paste_back=True,
            weight=0.5  # Balance between original and restored (0.5 is safe)
        )

        # --- Convert back to PIL (RGB) ---
        if restored_img_bgr is not None:
            restored_img_rgb = cv2.cvtColor(restored_img_bgr, cv2.COLOR_BGR2RGB)
            return Image.fromarray(restored_img_rgb)
        else:
            # Fallback if AI fails
            return pil_image