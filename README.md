This deep learning OCR project is aiming to recognize digital display contents which includes seven segment and bitmpap. 


Make custom dataset: 
- Make a directory named " VOC2007 ", contains three directory: " Annotations ", " ImageSets ", " JPEGImages ".
- Make sure "digit" directory contains the original 10 images
- ./augmenttaion.py
- ./annotation.py
- ./make_train_val_test.py 

Make rec dataset:   using img2rec.py:

	- Mkdir Images and Classify images into different folders
	- Cd myrec
	- python ./../../../MXNet-MKL-DNN/incubator-mxnet/tools/im2rec.py --list --recursive --train-ratio 0.9 ./data  ./../Images/  --pack-label
	(the .lst file generated this step has only three columns which does not satisfy the need of rec dataset format)
	- Touch update_lst.py 
	- Python update_lst.py
	(twice if for both train.lst and val.lst)
	- python ./../../../MXNet-MKL-DNN/incubator-mxnet/tools/im2rec.py --recursive --no-shuffle --train-ratio 0.9 --test-ratio 0.1 --num-thread 56 --quality 100 val.lst  ./../Images  --pack-label 
	(twice if for both train.lst and val.lst)

