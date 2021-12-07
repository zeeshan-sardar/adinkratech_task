# Sementic Segmentation ROS Node
This repository is related to the sementic segmentation paclaged in ROS node. 
The segmentation is done using classical image processing algoritm name watershed in opencv python. 

This node reads all the images placed in the "data" folder and passes them to the segmentation algorithm. These images are also published on a specified ROS topic. 

The algorothm segments the image and saves the results (overlayed images) in the "results" folder. These results are also published on their specific ROS topic. 

## Testing
This can be tested either directly running ROS node after setting up the environment or using the docker image created for this. 

The below steps are to run docker image. 

```
sudo docker run -it --rm --name rosseg ros-seg:latest 
```

Open a new terminal and enter the below commands to create a new instance and run ROS Master.

```
sudo docker exec -it rosseg bash
source ros_entrypoint.sh
roscore
```

Now go back to the previous terminal and run the node.

```
rosrun semseg semseg.py
```

After running successfully, the reslutant images can be seen in results folder.