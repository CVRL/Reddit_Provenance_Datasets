# Reddit Photoshop Battles Image Provenance Datasets #

![How a provenance case is generated](figure1.png?raw=true "Figure1")

DESCRIPTION:
************
Reddit photoshop battles (https://www.reddit.com/r/photoshopbattles/) is an online community that holds competitions to see who can generate the most amusing, relevant, or creative edited versions of original photos using tools such as Photoshop or GIMP.
Digital Image Provenance is the task of finding related and modified versions of an image and describing their relationships to an image in question (see [1]). The relationship between a set of images can be represented as a graph, with the nodes being images and directed edges as relationships. Image Provenance is an extension of Image Phylogeny [2]
Because contributors to the Reddit Photoshop battles often piggyback off of each other's work, their iterative edits to an original image provide perfect example cases for Image Provenance and Phylogeny related tasks.

OVERVIEW:
*********
Each provenance case is inferred using timestamps and parent-child relationships from the comment threads in which the images are posted. Each graph has a root node that is the original image provided for the battle.

REQUIREMENTS:
*************
Python2.7
urllib2
urlparse

USAGE:
******
JSON representations of each photoshop battle are located in the 'Datasets' folder.  Currently, we provide only the cases used in [1], located in the 'Datasets/TIP2018' folder. Newer and larger version of the dataset will be available shortly.

To generate the dataset, run:
python2 DownloadRedditDataset.py <json folder> -outputDir <output folder>

This will build a new folder structure located at the specified location, in which each photoshop battle case will be given a folder filled with its relevant images.

DISCLAIMER:
***********

While this dataset has been cleaned and scrubbed by hand, we provide no all content provided in dataset JSON files is downloaded at your own risk, and could contain not-safe-for-work material.

Not all images provided by dataset JSON files are openly licensed, please get creator's permission for use before utilizing this data.

JSON STRUCTURE
**************

Each graph case has a JSON file that describes its structure. the json format is as follows:


{
    "directed": true, 
    "title": "Graph Title"
    "links": [
        {
            "op": "none", 
            "source": 0, 
            "target": 1
        },
	{
            "op": "none", 
            "source": 1, 
            "target": 2
        }
    ], 
    "nodes": [
        {
            "URL": "http://i.imgur.com/Ie9ncOd.png", 
            "comment": "[Courtesy of Snagit Editor](http://imgur.com/Ie9ncOd)", 
            "date": "2016-03-16 15:46:30", 
            "file": "/media/jbrogan4/scratch2/Reddit_Prov_Dataset_v6/_Bored_child_waiting_in_line/g402_d12cwvk.png", 
            "fileid": "g402_d12cwvk.png", 
            "id": "g402_d12cwvk", 
            "seriesname": "g402_d12cwvk"
        }, 
        {
            "URL": "http://i.imgur.com/N3shRME.jpg", 
            "comment": "[If you say so!](http://i.imgur.com/N3shRME.jpg)\n\nEdit: Holy $%@&. My first Reddit gold. Thanks a lot!", 
            "date": "2016-03-16 16:31:29", 
            "file": "/media/jbrogan4/scratch2/Reddit_Prov_Dataset_v6/_Bored_child_waiting_in_line/g402_d12f0gr.jpg", 
            "fileid": "g402_d12f0gr.jpg", 
            "id": "g402_d12f0gr", 
            "seriesname": "g402_d12f0gr"
        }, 
        {
            "URL": "http://i.imgur.com/XOCiwjm.png", 
            "comment": "[Binding of Isaac Hush fight](http://i.imgur.com/XOCiwjm.png)", 
            "date": "2016-03-16 13:38:01", 
            "file": "/media/jbrogan4/scratch2/Reddit_Prov_Dataset_v6/_Bored_child_waiting_in_line/g402_d1275tq.png", 
            "fileid": "g402_d1275tq.png", 
            "id": "g402_d1275tq", 
            "seriesname": "g402_d1275tq"
        }

    ]
}

Source and target numbers for each edge within the 'links' list correspond to the ordered list index of each node in 'nodes'.

HOW TO CITE:
************
If you use this data in any way, please cite our work: 

@article{moreira2018image,
  title={Image Provenance Analysis at Scale},
  author={Moreira, Daniel and Bharati, Aparna and Brogan, Joel and Pinto, Allan and Parowski, Michael and Bowyer, Kevin W and Flynn, Patrick J and Rocha, Anderson and Scheirer, Walter J},
  journal={arXiv preprint arXiv:1801.06510},
  year={2018}
}

CITATIONS:
**********

[1] Moreira, D., Bharati, A., Brogan, J., Pinto, A., Parowski, M., Bowyer, K. W., ... & Scheirer, W. J. (2018). Image Provenance Analysis at Scale. arXiv preprint arXiv:1801.06510.
[2] Dias, Z., Rocha, A., & Goldenstein, S. (2010, December). First steps toward image phylogeny. In Information Forensics and Security (WIFS), 2010 IEEE International Workshop on (pp. 1-6). IEEE.
