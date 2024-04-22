sudo xlnx-config --xmutil loadapp nlp-smartvision
cd Face_Detect
source build.sh
sudo ./test_video_facedetect densebox_640_360.xmodel 0
