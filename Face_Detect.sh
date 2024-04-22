sudo xlnx-config --xmutil loadapp nlp-smartvision
visiocutie
source build.sh
cd Face_Detect
sudo ./test_video_facedetect densebox_640_360.xmodel 0
visiocutie
