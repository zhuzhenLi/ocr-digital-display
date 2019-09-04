This deep learning OCR project is aiming to recognize digital display contents which includes seven segment and bitmpap. 

Please note that training is conducing under gluon-cv/docs/tutorials/detection/ from official gluon-cv repo: 
https://github.com/dmlc/gluon-cv

STEP1: Dataset preparation: 
    
    - Generate customized dataset
        cd ocr-ledsegment-bitmap/text_gen/TextRecognitionDataGenerator
	    python run.py -f 64 -l num -c 8000 --length 8 -k 5 -wd -5 -tc '#000000','#999999' -m 20,20,20,20 -bl 0
	    python gen_voc_ann.py

           
    - Make sure here is no VOC2019 dataset already exist 
        cd ocr-ledsegment-bitmap/
        rm -r VOC2019

	- Generate VOC dataset
	    python make_voc.py
	    python make_train_val_test.py



STEP2: Pass dataset to Network:

    - Make sure here is no VOC2019 dataset already exist
        cd gluon-cv/docs/tutorials/detection/
	    rm -r VOC2019
        cp -r ~/ocr-ledsegment-bitmap/VOC2019/ ./



STEP3: Training:
     
        source /opt/intel/compilers_and_libraries/linux/bin/compilervars.sh intel64
        export PYTHONPATH=~/MXNet-MKL-DNN/incubator-mxnet/python/

        rm -r number_train_result/
        python train_ssd.py --save-prefix number_train_result2/ --epochs 70 --batch-size 32 --lr 0.001 --lr-decay 0.1 --lr-decay-epoch 40,50,60

       



