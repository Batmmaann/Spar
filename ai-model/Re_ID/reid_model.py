import torch
import torchreid
from torchvision import transforms
import cv2
import numpy as np

class ReIDModel:
    def __init__(self, device='cuda'):
        self.device = device if torch.cuda.is_available() else 'cpu'
        
        self.model = torchreid.models.build_model(
            name='osnet_ain_x1_0', num_classes=1000, pretrained=True
        )
        self.model.to(self.device)
        self.model.eval()

        
        self.transform = transforms.Compose([
            transforms.ToPILImage(),              
            transforms.Resize((256, 128)),          
            transforms.ToTensor(),                  
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),  
        ])

    def extract_embedding(self, image):
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = self.transform(image_rgb).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(input_tensor)
        embedding = embedding.cpu().numpy().flatten()
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding

def preprocess(crop):
   
    return crop
