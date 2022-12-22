# Edge-Cloud-simulator
This is a simulator which used to explore the performance inversion problem reported in [paper]: https://arxiv.org/abs/2104.14050  

## Set the enviroment  
python3.7  

pybind11==2.10.1  

scipy==1.2.1  

Pyqt5  

matplotlib==3.0.3  

g++ 7.5.0  

## Compile scheduler module  
after the python enviroment is ready, Compile the FCFS module(implemented by C++ and pybind)  

cd cpp_src  

sh run.sh  

## Using GUI to do simulation  
then you can go to the root path of the repo  

python GUI_simulation.py  
Then the GUI would be displayed on the screen, you can set the parameters and go on with the simulation  

![Gui](./img/GUI)
