# Sementic Segmentation ROS Node
This repository is related to the sementic segmentation using two different approaches desribed.
### Classical Approach
This segmentation is done using watershed segmentation algorithms in Python OpenCV. This is packaged in ROS Node and containerized to make it portable and easy to test.

### Deeplearning Approach
This approach is using the state-of-art segmentation techniques. The primary implmentation is done by [MIT CSAILVision Lab ](https://github.com/CSAILVision/semantic-segmentation-pytorch) on [MIT ADE20K](http://sceneparsing.csail.mit.edu/) dataset. 

This is not packaged in ROS as it was tested using Google Colab and running ROS on Colab is itself a task.


## Testing

### Segmentation in ROS Node using Watershed Algorithm
This can be tested either directly running ROS node after setting up the environment or using the docker image created for this. 

The below steps are to run docker image. 

Run the docker image. For the first run, it will pull the image from docker hub once done it will run without that. 

```
sudo docker run -it --rm --name rosseg ros-seg:latest 
```

Open a new terminal and enter the below commands to create a new instance and run ROS Master.

```
sudo docker exec -it rosseg bash
source ros_entrypoint.sh
roscore
```

Now go back to the previous terminal and launch the node.

```
roslaunch semseg semseg.launch
```

Once you launch the node, you should be able to see two ROS topics named `input_images` and `results` for both the input images and output results respectivly. 


By default the input images are read from `data` folder inside the package (semseg) and the results are stored in `results` folder inside the package. These directories can be changed by passing the arugment while launching the launch file. For example

```
roslaunch semseg semseg.launch imgdir:="your input location"
roslaunch semseg semseg.launch resultdir:="your result location"
```

If you wish to run it locally (out of docker container), then build the catkin project and launch the same launch file described above. 



### Segmentation using DeepLearning Model
This deeplearning based model is good at segmentation and produces accurate results. The problem is that it requires GPU to run. I tried it on 2GB Nvidia GPU but the memory was not sufficient to run it. 

That being said, I am not able to run on local machine and Google Colab was the only option. But Colab does not support ROS well and that is why I am unable to make a ROS package out of it. 

So, here is the notebook link [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12LDNcFgjaghc410AwykpN8n8Wip4Kejy?usp=sharing) . All the instructions are written in the notebook.