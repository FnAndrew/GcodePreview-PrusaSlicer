
# G-code Preview for PrusaSlicer

Remake of [MKS plugin](https://github.com/PrintMakerLab/mks-wifi-plugin) and it's [MKSPreview.py](https://github.com/PrintMakerLab/mks-wifi-plugin/blob/develop/MKSPreview.py) file to make a print preview in PrusaSlicer


## How it works

The original script uses Cura's [Snapshot](https://github.com/Ultimaker/Cura/blob/main/cura/Snapshot.py) class to make a screenshot of a model.

We edited it to extract the PrusaSlicer's G-code thumbnail and ussing Post-processing script it's edited and added to the G-code in the corresponding format.

## Ussage

1. Go to `Printers > General > Firmware > G-code thumbnails` and insert `400x300/PNG`. Now the slicer will make a screenshot of a model each time you Export it.

![Thumbnail settings](/assets/thumbnail-settings.png)

2. Get a full path of this script. Something like `python-to-file\GcodePreviewAdder.py`

3. Get a full path of a Python executable. Something like `C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe`

4. Now you can go to `Print Settings > Output options > Post-processing scripts` and insert the Python and script paths in quotes like:

`"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Python 3.9" "C:\path-to-file\GcodePreview\GcodePreviewAdder.py"`

![Script settings](/assets/script-settings.png)

5. Enjoy! Now the slicer will add a preview of a model on the Export

![Preview showcase](/assets/preview-showcase.png)


## FAQ

#### Q: I got an error code 1 when exporting

A: Most likely your Python interpreter doesn't have installed the libraries.

1. With thu full Python path run this: 
```bash
  "full-python-path\python.exe" -m pip list
```

2. If you get an error `No module named 'pip'`, then download `https://bootstrap.pypa.io/get-pip.py` and run it with your interpreter.
```bash
  "full-python-path\python.exe" "full-path-to-the-get-pip.py"
```

Now the step 1 should work :D

3. When the step 1 is working and there isn't listed the `PyQt5` library. Install it ussing
```bash
  "full-python-path\python.exe" -m pip install PyQt5
```

#### Q: It doesn't work for my printer

Our remake of this script uses Default configuration of the plugin and it can be remade for any other configuration.

Just rewrite the values in the `generate_preview(image)` function according to your needs.

```json
  [
    { "index": 1, "label": "Default", "simage": "100", "gimage": "200", "encoded": false },
    { "index": 2, "label": "FLSUN QQ-S", "simage": "", "gimage": "" , "encoded": false },
    { "index": 3, "label": "Flying Bear Ghost 4S/5", "simage": "50", "gimage": "200", "encoded": false },
    { "index": 4, "label": "Two Trees Sapphire", "simage": "100", "gimage": "200" , "encoded": false },
    { "index": 5, "label": "Wanhao D12", "simage": "100", "gimage": "200" , "encoded": false },
    { "index": 6, "label": "Artillery Sidewinder X3", "simage": "85", "gimage": "230", "mimage": "170", "encoded": true  },
    { "index": 7, "label": "Elegoo Neptune2 | NeptureX", "simage": "100", "gimage": "200", "encoded": true  },
    { "index": 8, "label": "Elegoo Neptune3+", "simage": "160", "gimage": "200", "encoded": true  }
]
```

#### Common examples of wrong configuration:
When there is no `gimage`:
![gimage showcase1](/assets/gimage-showcase1.png)

When there is too small `gimage`:
![gimage showcase1](/assets/gimage-showcase2.png)