Name:
3D Graphing Calculator

Description:
Graphs 3D functions of the forms x=f(y,z), y=f(x,z), and z=f(x,y);
Graphs parametrics with two parameters
Graphs parametrics with one parameter
Can handle multiple graphs of each type simultaneously

How to run:
Open MainFile.py and run it as a script

Installing libraries:
None

Shortcuts:
None
There are sample graphs that are commented in the model section of MainFile.py
There are useful keyboard commands, which can be seen when the Help box is clicked. These are not shortcuts though.


The format for a function is:
dependent variable = expression
rgbColor

Ex:
z=sinx+siny-3
(100,0,0)

The format for a parametric (2 parameters), with t and u as parameters, is:
x=expression
y=expression
z=expression
t_min,t_max,t_step
u_min,u_max,u_step
rgbColor

Ex (torus):
x=(4+cost)*cosu
y=(4+cost)*sinu
z=sint
0,2*pi,pi/10
0,2*pi,pi/15
(0,100,0)

The format for a parametric (1 parameter), with t as the parameter, is:
x=expression
y=expression
z=expression
t_min,t_max,t_step
rgbColor

Ex (helix):
x=cost
y=sint
z=t
0,3*pi,pi/10
(200,100,0)