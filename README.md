# UVL_identification_FastSAM
 
#[0] Installation and Preparation

```shell
	#cd to this directory

cd ./ultralytics-main
pip install -e .
cd..           # Return to the previous directory

#[1] Prepare Dataset
    #Please download a COCO dataset for training and validation. The UVL coco dataset made by this research can be downloaded at Figshare.
	#For detailed content, see https://docs.ultralytics.com/datasets/segment/coco/


#[2] Training

python train.py

	#Check if the address specified in train.py is correct.
	#Parameters can be adjusted; refer to the YoloV8 documentation. The default model is currently 'best1_FastSAM_100.pt', but can be changed anytime.
    FastSAM model for training can be downloaded at: 
    FastSAM-x.pt: https://drive.google.com/file/d/1m1sjY4ihXBU1fZXdQ-Xdj-mDltW-2Rqv/view
    FastSAM-s.pt: https://drive.google.com/file/d/10XmSj6mmpmRb8NhXbtiuO9cTTBwR_9SV/view
    More information about FastSAM model: https://github.com/CASIA-IVA-Lab/FastSAM
# If you want to train your own model, please place the downloaded model (e.g., FastSAM-s.pt) in this folder and modify the code in train.py as follows:
if __name__ == '__main__':
    model = YOLO("FastSAM-s.pt")
    model.load("FastSAM-s.pt")


#[3] Validation

python val.py

	#Parameters can be adjusted.
	#Output is located under the project and name parameters.

	#[4] Prediction
	#Note: The default prediction model is the pre-trained model from the research.
	#Place images for prediction in ./predict/images

python predict.py

	#Parameters can be adjusted.
	#For detailed parameters, see https://docs.ultralytics.com/modes/predict/#inference-arguments
	#Prediction results are saved in ./runs/segment/predict.
	#The prediction labels are stored in ./runs/segment/predict/labels as .txt files.


python yolo2mask.py  #Copy the .txt files to ./predict/labels and generate the mask results (PNG format) in ./predict/output.

