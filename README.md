# celegans-pergola-reproduce.nf

![CircleCI status](https://circleci.com/gh/cbcrg/celegans-pergola-reproduce.png?style=shield)
[![nextflow](https://img.shields.io/badge/nextflow-%E2%89%A50.20.0-brightgreen.svg)](http://nextflow.io)

This repository contains the software, scripts and data to reproduce the results corresponding to the *C.elegans* data of the Pergola paper.

## Clone the repository

```bash
git clone --recursive https://github.com/cbcrg/celegans-pergola-reproduce.git
cd celegans-pergola-reproduce
```

## Data

Data is publicly available in [Zenodo](https://zenodo.org/) as a compressed tarball [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1067834.svg)](https://doi.org/10.5281/zenodo.1067834).

Data can be downloaded and uncompressed using the following command:

```bash
mkdir data
wget -O- https://zenodo.org/record/1067834/files/celegans_dataset.tar.gz | tar xz -C data
```

#### Original Data Sources

~~If you prefer, you can download the data from the original sources~~:
~~N2 C.elegans strain (control) behavioral recordings: [N2](http://wormbehavior.mrc-lmb.cam.ac.uk/strain.php?strain=300)~~
~~unc-16 C.elegans strain behavioral recordings: [unc-16](http://wormbehavior.mrc-lmb.cam.ac.uk/strain.php?strain=1)~~

The database has been migrated and the data can now be accessed at this [link](http://movement.openworm.org/) 

**Note**: Only a subset of the N2 files available on the database, those recorded within a 2-week window centered around the unc-16 mutant strain, have been used for the analysis. The detailed list of files is:

```bash
N2 on food L_2009_12_09__10_31_26___6___1_features.mat
N2 on food L_2009_12_09__10_31_54___4___1_features.mat
N2 on food L_2009_12_10__10_20_00___1___1_features.mat
N2 on food L_2009_12_10__10_20_40___6___1_features.mat
N2 on food L_2009_12_10__10_20___3___1_features.mat
N2 on food L_2009_12_10__10_21_10___4___1_features.mat
N2 on food L_2009_12_10__10_22_01___7___1_features.mat
N2 on food L_2009_12_11__12_03_49___8___1_features.mat
N2 on food L_2009_12_11__12_04_46__1_features.mat
N2 on food L_2009_12_14__10_21___3___1_features.mat
N2 on food L_2009_12_14__10_22_12___8___1_features.mat
N2 on food L_2009_12_14__10_22_30___7___1_features.mat
N2 on food L_2009_12_15__10_22_57___2___1_features.mat
N2 on food L_2009_12_15__10_22___3___1_features.mat
N2 on food L_2009_12_15__10_23_42___8___1_features.mat
N2 on food L_2009_12_15__10_24_35__1_features.mat
N2 on food L_2009_12_17__11_02_29___1___1_features.mat
N2 on food L_2009_12_17__11_03_15___6___1_features.mat
N2 on food L_2009_12_17__11_03_42___4___1_features.mat
N2 on food L_2009_12_17__11_05_22___7___2_features.mat
N2 on food R_2009_12_09__10_30_41___1___1_features.mat
N2 on food R_2009_12_09__10_31_25___2___1_features.mat
N2 on food R_2009_12_09__10_31___3___1_features.mat
N2 on food R_2009_12_09__10_32_28___8___1_features.mat
N2 on food R_2009_12_10__10_20_42___2___1_features.mat
N2 on food R_2009_12_10__10_21_43___8___1_features.mat
N2 on food R_2009_12_11__12_01_09___1___1_features.mat
N2 on food R_2009_12_11__12_01_52___2___1_features.mat
N2 on food R_2009_12_11__12_01___3___1_features.mat
N2 on food R_2009_12_11__12_04_07___7___1_features.mat
N2 on food R_2009_12_14__10_20_23___1___2_features.mat
N2 on food R_2009_12_14__10_21_06___2___2_features.mat
N2 on food R_2009_12_14__10_21_38___4___1_features.mat
N2 on food R_2009_12_14__10_23_04__1_features.mat
N2 on food R_2009_12_15__10_21_50___1___1_features.mat
N2 on food R_2009_12_15__10_22_39___6___1_features.mat
N2 on food R_2009_12_15__10_23_59___7___1_features.mat
N2 on food R_2009_12_17__11_04_16___8___1_features.mat
N2 on food_2009_12_09__10_32_45___7___1_features.mat
N2 on food_2009_12_09__10_33_20__1_features.mat
```

If you have not install yet [docker](https://www.docker.com/) and [nextflow](https://www.nextflow.io/), follow this [intructions](https://github.com/cbcrg/pergola-reproduce/blob/master/README.md)

## Pull docker image
Pull the Docker image use for processing data with Pergola (Pergola and its dependencies installed)

```bash
docker pull pergola/pergola@sha256:f7208e45e761dc0cfd3e3915237eb1a96eead6dfa9c8f3a5b2414de9b8df3a3d
```

## Run nextflow pipeline
Once data is downloaded, it is possible to reproduce all the paper results using this command:

```bash
NXF_VER=0.26.1 nextflow run celegans-pergola-reproduce.nf \
    --strain1_trackings 'data/unc_16/*.mat' \
    --strain2_trackings 'data/N2/*.mat' \
    --mappings_speed 'data/mappings/worms_speed2p.txt' \
    --mappings_bed 'data/mappings/bed2pergola.txt' \
    --mappings_motion data/mappings/worms_motion2p.txt \
    -with-docker
```	

##  Results

The nextflow pipeline produces a results folder containing:

* Three plots comparing the distribution of *unc-16* and *N2* mid body speed when moving forward, backward and when paused, respectively.  
* A figure created using [Gviz](https://bioconductor.org/packages/release/bioc/html/Gviz.html) depicting in a heatmap the mid body speed of *unc-16* and *N2* *C.elegans* strains.
* A figure created using [Sushi](https://bioconductor.org/packages/release/bioc/html/Sushi.html) rendering in a heatmap the mid body speed of *unc-16* and *N2* *C.elegans* strains.
* A folder containing all the necessary files to compare mid body speed of the two strains in a heatmap using [IGV](http://software.broadinstitute.org/software/igv/). Data is separated in folders corresponding to each mouse group.
See [below](IGV-visualization) for a detailed explanation of how to load the data on IGV.


## IGV visualization
You can use the version we adapted of the [Integrative Genomics Viewer](http://software.broadinstitute.org/software/igv/) (or the original one) to browse the resulting data (as we did for the paper).
However IGV does not allow extended programatic access to set the graphical options, hence our script produces a heatmap reproducing the paper figure. This file can be found inside the ``heatmap`` results folder.

#### Adapted IGV version
We adapted IGV to display temporal data incorporating minor changes. To do so we fork the [IGV](https://github.com/igvteam/igv) git repository into but we call IBB (Integrative Behavioral Browser)

You can clone and build IBB using the following commands:

**Note**: If you prefer to use the original IGV you can download from [here](https://software.broadinstitute.org/software/igv/download)

```bash
git clone --recursive https://github.com/JoseEspinosa/IBB.git

cd IBB/
ant -f build.xml
./ibb.sh
```

Go to the menu **Genomes --> Create .genome File ..**
Select the fasta file created in the ``results/igv`` folder and click on OK and save the genome in your system as shown in the snapshot below:

<img src="/images/create_genome.png" alt="snapshot create-genome" style="width: 100%;"/>

Open the tracks in ``.bedGraph`` format from the ``/results/igv/results_bedgr1_igv`` folder from the menu **File --> Load from File...**

Select all the tracks clicking on their name and right click to display options, and select the options as in the snaphot below:

<img src="/images/track_options.png" alt="snapshot create-genome" style="width: 50%;"/>

Do the same with the data of the *N2* strain placed inside ``/results/igv/results_bedgr2_igv``. 
 
Finally click on the same menu the **Set Heatmap Scale** option and select the configure it as in the image:

<img src="/images/heatmap_options.png" alt="snapshot create-genome" style="width: 100%;"/>
 
