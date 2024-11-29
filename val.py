from ultralytics import YOLO
model = YOLO(model="Model/best1_FastSAM_100.pt", \
             )
model.val(data="Datasets/UVL_data.yaml", \
            epochs=100, \
            batch=1, \
            imgsz=512, \
            device='0',\
            project='FastSAM', \
            name='FastSAM_for_UVL', 
            val=False,
            save_json=True, \
            conf=0.0001, \
            iou=0.9, \
            max_det=100, \
            )
