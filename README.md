# Edge-Cloud-simulator
This is a simulator which used to explore the performance inversion problem reported in [paper]: https://arxiv.org/abs/2104.14050  

Set the enviroment
--------
python3.7  

pybind11==2.10.1  

scipy==1.2.1  

Pyqt5  

matplotlib==3.0.3  

g++ 7.5.0  


after the python enviroment is ready, Compile the FCFS module(implemented by C++ and pybind)  

cd cpp_src  

sh run.sh  


then you can go to the root path of the repo  

python GUI_simulation.py
![Gui](./img/GUI)
