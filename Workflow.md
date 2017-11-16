# IHCount pipeline

## Use python script for batch processing

Start [runCP.py](/runCP.py) in the command line

```bash
> python runCP.py
```
#### Step 1: Image preprocessing

Step 1 extracts the layer with the highest resolution (default is 0) from the image container [Aperio, Leica,....] and saves it as .tif. The image gets tiled into smaller subimages [2000x2000 px], saved in a subdirectory (imageX.tiles). 

```bash
>>> preprocess [Press Enter]
```

#### Step 1: Image preprocessing for single image

Choose series with the highest resolution (default is 0).

```bash

> ./bftools/showinf -nopix imageX.tif

> ./bftools/bfconvert -tilex 512 -tiley 512 -series 0 -compression LZW imageX.[svs, scn, ...] imageX.tif

> ./bftools/bfconvert -debug -tilex 2000 -tiley 2000 imageID.tif imageX.tiles/imageX.X%x.Y%y.tile.tissue.tif

```
After that, the directory structure should look like this

```bash

├── root/
│   ├── bftools/
│   ├── runCP.py
│   ├── image1.svs[scn,....]
│   ├── image1.tif
│   ├── image1.tiles/
│   │   ├── image1.X0.Y0.tissue.tile.tif
│   │   ├── image1.X1.Y0.tissue.tile.tif
│   │   ├── .........
│   │   └── image1.X35.Y20.tissue.tile.tif
│   │ 
│   ├── image2.svs[scn,....]
│   ├── image2.tif
│   ├── image2.tiles/
│   │   ├── image2.X0.Y0.tissue.tile.tif
│   │   ├── image2.X1.Y0.tissue.tile.tif

```

#### Step 2: Training and classification of positively stained cells

Start Ilastik application and create a project file (*.ilp). Use the <b>Pixel Classificator</b> module and annotate the classes (e.g. CD8 positives, tissue, background, nuclei) we want to identify on the IHC-image.

As training data, use a subset of the previously created image tiles. For the different classes we used red, blue and green as color codes. We created two classifiers: 

* The classifier <b>nuclei</b>, is trained to distinguish background [blue], tissue [green] and nuclei [red].

* The classifier <b>positives</b> was trained on background [blue], tissue (includes also non-positive nuclei) [green] and positively stained nuclei (CD8,CD4,...) [red].

<p align="center">
  <img width="281" height="185" src="https://github.com/mui-icbi/IHCount/blob/master/images/annotation.png?raw=true" alt="positives"/>
</p>

Run a batch process on all image tiles in the directory <b>imageX.tiles</b> and export a probability map for each of tile into this directory.  


#### Step 3: Counting cells and extracting spatial features

Create a text file <b>fileList.txt</b> containing the absolute path for each image tile, which is needed for further processing steps using CellProfiler.

```bash
>>> list [Press Enter]
```

```bash

├── root/
│   ├── runCP.py
│   ├── image1.svs[scn,....]
│   ├── image1.tif
│   ├── image1.tiles/
│   │   ├── fileList.txt
│   │   ├── image1.X0.Y0.tile.tissue.png
│   │   ├── image1.X1.Y0.tile.nuclei.tif
│   │   ├── image1.X1.Y0.tile.positives.tif
│   │   ├── .........
│   │   └── image1.X35.Y20.tile.tissue.png
│   │ 
│   ├── image2.svs[scn,....]
│   ├── image2.tif
│   ├── image2.tiles/
│   │   ├── fileList.txt
│   │   ├── image2.X0.Y0....
│   │  

```

The segmentation and object detection was conducted by <b>CellProfiler</b> using the [IHCount.cppipe](/IHCount.cppipe) pipeline. You can call CellProfiler either in the GUI or from the command line [runCP.py](/runCP.py)

```bash
>>> count [Press Enter]
```
as single command 

```bash

> cellprofiler -c -r -o /output Path -p /.cppipe file Path --file-list /fileList.txt Path

```

#### Step 4: Summarise result tables

```bash
>>> summarise [Press Enter]
```

The IHCount pipeline exports a <b>result_Image.csv</b> file, which contains the cell counts and object features for each single tile. The counts for each single tile will be summed up to a total count for the whole image and saved in results_count.csv.

```bash

├── root/
│   ├── results_count.csv
│   ├── runCP.py
│   ├── image1.svs[scn,....]
│   ├── image1.tif
│   ├── image1.tiles/
│   │   ├── result/
│   │   │   ├── result_Image.csv
│   │   │   ├── result_Nuclei.csv
│   │   │   ├── result_Positives.csv
│   │   ├── fileList.txt
│   │   ├── image1.X0.Y0.tile.tissue.png
│   │   ├── image1.X1.Y0.tile.nuclei.tif
│   │   ├── image1.X1.Y0.tile.positives.tif
│   │   ├── .........
│   │   └── image1.X35.Y20.tile.tissue.png
│   │ 
│   ├── image2.svs[scn,....]
│   ├── image2.tif
│   ├── image2.tiles/
│   │   ├── fileList.txt
│   │   ├── image2.X0.Y0....
│   │  

```

The files <b>result_Nuclei.csv</b> and <b>result_Positives.csv</b> contain information about location of the objects on the analysed tile, which can be used for additional spatial analysis.
