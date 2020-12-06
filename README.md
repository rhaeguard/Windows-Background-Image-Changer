# Background image changer

### Steps


- #### Setting environment variables

`WBC_IMAGES_DIR` is the folder to save the background images to. `WBC_UNSPLASH_CID` is the Unsplash API access key.

- #### `launcher.bat` file

```
python script.py
```

and add this bat file as a scheduled task in Task Scheduler. The file should be located in system drive (otherwise access should be granted)

```
cmd /c launcher.bat >> wbc.log 2>&1
```