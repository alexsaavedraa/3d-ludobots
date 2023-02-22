# 3d-ludobots
generates shambling almagamations using this code. run using snakes.bat

THIS IS BASED OFF OF R/LUDOBOTS. LARGE PORTIONS OF THIS CODEBASE ARE DIRECTLY TAKEN FROM THE SUBREDDIT. 


Here we generate a 3d ludobot and corresponding brain. The pictured diagram shows the first steps of generating, with green being a sensor and blue being a normal cube:
![image](https://user-images.githubusercontent.com/114758213/220529465-0ca1cad0-c0ed-4382-a8b1-4aaffe8babb0.png)
The first step starts with the head block, with ID of one.
The second step randomly chooses a face, then attatches a block to it. 
Each next step chooses a face from all available faces and attatches a block to it. A face is available if it has no other blocks attatched. this process is repeated until the number of blocks specified is reached.
![image](https://user-images.githubusercontent.com/114758213/220530775-6d9b4711-5f5b-4a44-b2b9-02e007d0d972.png)
This image shows how the brain is created. red circles are sensor neurons, dark red lines are motor neurons, and pink/purple lines are synapses. 


