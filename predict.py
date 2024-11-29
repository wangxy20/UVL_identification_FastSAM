from ultralytics import YOLO
import os
import argparse

parser = argparse.ArgumentParser(description='test')
parser.add_argument('--path', type=str, default='./predict/images', help='the path of images needed to be predicted 需要预测图片的地址')
parser.add_argument('--model', type=str, default='./Model/best1_FastSAM_100.pt', help='model path for predict 预测模型的地址')
args = parser.parse_args()
print(args.path)

if __name__ == '__main__':
    model = YOLO(args.model)
    model.load(args.model)

results = model.predict(source = args.path, 
                        save = True, 
                        save_txt = True,
                        imgsz = 512,
                        )

os.kill()

        
