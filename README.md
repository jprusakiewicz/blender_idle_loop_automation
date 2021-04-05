# Blender idle loop automation using python API 🐍

## How to use

Add Blender to env path 
https://docs.blender.org/manual/en/2.93/advanced/command_line/launch/windows.html

Run `pip install -r code/requirements.txt`to install dependencies  

add (one or many) _.fbx_ files to **source** folder  
Go to **code** folder  
Run `python main.py `in console.  


## user configuration 
####There are several parameters user can set in config.py file:

* import_scale - imported _.fbx_ object scale
* start_frame - frame beginning the idle loop
* end_frame - frame ending the base idle loop
* last_key_frames_ahead - distance to copy-paste first base key of the loop after its last base key.

##### All of the following paths are referenced starting from code directory
* core_path - core.py file path  
* source_fbx_directory_path - directory path where will be preplaced source .fbx files  
* export_directory_path - directory where will be exported processed .fbx files  
* export_suffix - every exported .fbx file name suffix
   

## Going short with only one _.fbx_ file  
 ####(optional)
If you want to process only one .fbx file you can use `core.py` file with _Blender_ command.
It takes 4 arguments: import scale, source fbx file path, export directory path, export suffix  
example:  
`Blender ../target/target.blend --background --python core.py -- 1 ../source/ ../exports _DONE 200 650 30 <path_to_better_fbx_addon_zip>`


## idle loop process step by step  
1. set object mode  
2. import fbx with scale=x using better fbx  
3. select collection "Armature"  
4. set object mode  
5. get all fcurves from animation
6. remove all keyframe points not in loop range
7. copy-paste keys from first frame to (last frame + ahead distance)
8. set overall scene frame range
9. export fbx



## Blender env path troubleshooting
Depending how you set your _blenderpath_ you may want to change first capital letter in Blender command.
To do this replace it in main.py:24 
In my case it works with both '**blender**' and '**Blender**' (big and small letter)

## Error logs
If there is any error produced by user, preventing code to work properly 
(e.g. wrong user configuration) message will be logged.
Be aware that it doesn't have to be located at the end of output.  
![](https://imgur.com/eDaJ04t)


1.0 version tested on 2.91.0 Blender version  
Made with 🧠 by Jakub Prusakiewicz