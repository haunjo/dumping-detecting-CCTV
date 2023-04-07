from pathlib import Path
import os

import torch

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, apply_classifier, scale_coords, set_logging
from utils.torch_utils import select_device, load_classifier

class Detector():
    def __init__(self):
        self.weights = 'yolov7.pt'  # 'model.pt path(s)'
        self.imgsz = 320  # 'inference size (pixels)'
        self.conf_thres = 0.25  # 'object confidence threshold
        self.iou_thres = 0.45  # 'IOU threshold for NMS'
        self.classes = None  # 'filter by class: --class 0, or --class 0 2 3'
        self.augment = False  # 'augmented inference'
        self.agnostic_nms = False  # 'class-agnostic NMS'
        set_logging()
        self.device = select_device('')  # 'cuda device, i.e. 0 or 0,1,2,3 or cpu'
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        
        # Load model
        self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(self.imgsz, s=self.stride)  # check img_size
        
        if self.half:
            self.model.half()  # to FP16
            
        # Second-stage classifier
        self.classify = False
        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            self.modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()

        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once
        self.old_img_w = self.old_img_h = self.imgsz
        self.old_img_b = 1
        
    def detect(self, source):
        # Set Dataloader
        self.dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride)

        # Run inference
        for path, img, im0s, _ in self.dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if self.device.type != 'cpu' and (self.old_img_b != img.shape[0] or self.old_img_h != img.shape[2] or self.old_img_w != img.shape[3]):
                self.old_img_b = img.shape[0]
                self.old_img_h = img.shape[2]
                self.old_img_w = img.shape[3]
                for _ in range(3):
                    self.model(img, augment=self.augment)[0]

            # Inference
            with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
                self.pred = self.model(img, augment=self.augment)[0]

            # Apply NMS
            self.pred = non_max_suppression(self.pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=self.agnostic_nms)

            # Apply Classifier
            if self.classify:
                self.pred = apply_classifier(self.pred, self.modelc, img, im0s)

            # Process detections
            has_person = 0 
            for det in self.pred:  # detections per image
                p, im0 = path, im0s

                p = Path(p)  # to Path
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
 
                    # Print results
                    for c in det[:, -1].unique():
                        if not has_person and self.names[int(c)] == 'person':
                            has_person = 1
            
            # remove the image if it has no any person.
            if not has_person:
                try:
                    os.remove(path)
                    print("the image is removed.")
                except FileNotFoundError as e:
                    print(e)