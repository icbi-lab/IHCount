# IHCount workflow

This is a general workflow, used for the quantitative analysis of multiple IHC-Images. The pipeline we setup for this analysis utilises several publicly available tools for the different steps of pre-processing ([Python](https://www.python.org/download/releases/2.7/)<sup>1</sup>, [bftools](https://docs.openmicroscopy.org/bio-formats/5.7.1/users/comlinetools/index.html)<sup>2</sup>, [libvips](http://www.vips.ecs.soton.ac.uk)<sup>3</sup>), classification([Ilastik](http://ilastik.org/download.html)<sup>4</sup>) and segmentation ([CellProfiler](http://cellprofiler.org)<sup>5</sup>). The individual steps of this workflow were combined in a python script [runCP.py](/runCP.py), which is easy to adapt. 


#### Preprocessing

For the preparation of the IHC-images for further analysis, we used the script collection bftools from the [OME - Bio-Formats](https://www.ncbi.nlm.nih.gov/pubmed/20513764)<sup>6</sup>. As a first step, high-resolution bright-field images were extracted from the image containers available in Leica (SCN) format. Following this, each of these high-resolution images was tiled into smaller subimages, which can be used as training data.

![alt text](/images/preprocessing.jpg)


#### Classification

The Pixel Classificator module of Ilastik was used to establish classifiers from a subset of the previously
generated image tiles. Using manual annotation, the classifiers were trained to distinguish positively stained
cells and all nuclei on the selected IHC-Images, as well as tissue and background. As a result of running the
classifier as a batch process on all tiles of a slide, we obtained two sets of so called probability maps. One set shows
the probabilities for positively stained cells and the second for all nuclei on the slide, together with the probabilities for stromal tissue and background. These maps were used
in the following segmentation and quantification steps.

![alt text](/images/classification_workflow.jpg)


#### Cell counting and extraction of spatial features

The cell segmentation and counting, as the final steps in this workflow, were performed by CellProfiler. The probability maps together with the original tiles 
were loaded into CellProfiler, either using the GUI or running it from the command line. We created a pipeline ([IHCount.cppipe](/IHCount.cppipe)) that utilises several intensity based modules for image processing to identify and quantify positive stained cells, nuclei and the area of tissue.

![alt text](/images/cp_workflow.jpg)


#### Tools used

1. [Python 2.7](https://www.python.org/download/releases/2.7/) - Python 2.7
2. [bftools](https://docs.openmicroscopy.org/bio-formats/5.7.1/users/comlinetools/index.html) - OME command line tools for image processing 
3. [VIPS Project](http://www.vips.ecs.soton.ac.uk) - Image processing library
4. [Ilastik 1.2.2](http://ilastik.org/download.html) - Interactive learning and segmentation toolkit
5. [CellProfiler 2.2.0](http://cellprofiler.org) - Cell image analysis software
6. [OME - Bio-Formats](https://www.ncbi.nlm.nih.gov/pubmed/20513764) Linkert, M. et al. Metadata matters: access to image data in the real world. J. Cell Biol. 189, 777–782 (2010)
