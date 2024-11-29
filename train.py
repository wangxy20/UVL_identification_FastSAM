from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO("FastSAM-s.pt")
    model.load("FastSAM-s.pt")
    model.train(data="Datasets/UVL_data1.yaml", \
                epochs=100, \
                batch=16, \
                imgsz=512, \
                overlap_mask=False, \
                save=True, \
                save_period=25, \
                device='0',\
                project='FastSAM', \
                name='Fast_data1', 
                val=False,)