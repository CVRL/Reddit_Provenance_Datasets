import os
import sys
import json
import urlparse
import urllib2

def addTitlesToJson(dataDir):
    if not dataDir.endswith('/'): dataDir += '/'
    jsonDir = os.path.join(dataDir,'..','jsons')
    for root,dirs,files in os.walk(dataDir):
        dirname = root[len(dataDir):]
        for f in files:
            if f.endswith('.json') and not f.startswith('graph'):
                with open(os.path.join(root,f),'r') as fp:
                    graph = json.load(fp)
                if 'title' not in graph:
                    graph['title'] = dirname
                    with open(os.path.join(root, f), 'w') as fp:
                        json.dump(graph,fp)
                    with open(os.path.join(jsonDir, f), 'w') as fp:
                        json.dump(graph,fp)

def downloadImages(image_urls,image_names,out_dir):
    print("Scanning URLs...")

    # Create an output directory
    try:
        os.makedirs(out_dir)
    except:
        pass #print "Error creating directory",out_dir

    imageNameList = {}
    i = 0
    count = 0
    for j in range(len(image_urls)):
        each0 = image_urls[j]
        bn = urlparse.urlsplit(each0).path.split('/')[-1]
        imgName = image_names[j]
        out_path = os.path.join(out_dir, imgName)
        shouldAdd = True
        if not os.path.exists(out_path):
            try:
                print("Reading URL:",each0)
                f = urllib2.urlopen(each0,timeout=10)
                data = f.read()
                f.close()
                print("   Datasize:",len(data))
                if len(data) > 600:
                    f = open(out_path,'wb')
                    f.write(data)
                    f.close()
                    i+=1
                else:
                    shouldAdd = False

            except KeyboardInterrupt:
                raise

            except:
                print ("Error Fetching URL:",each)
                imageNameList[each[1]] = (None,None,None)
                traceback.print_exc()
        count += 1

def downloadFromJson(gfile,outDir):
    imageURLList = []
    imageNameList = []
    with open(gfile,'r') as fp:
        jsonGraph = json.load(fp)
    for n in jsonGraph['nodes']:
        filename = os.path.basename(n['file'])
        url = n['URL']
        imageURLList.append(url)
        imageNameList.append(filename)
        n['file'] = os.path.join(outDir,jsonGraph['title'],filename)
    downloadImages(imageURLList,imageNameList,os.path.join(outDir,jsonGraph['title']))
    with open(os.path.join(outDir,jsonGraph['title'],os.path.basename(gfile)),'w') as fp:
        json.dump(jsonGraph,fp)
def downloadImagesforAllJsons(jsonDir,outDir):
    for f in os.listdir(jsonDir):
        if os.path.isfile(f) and f.endswith('.json'):
            downloadFromJson(os.path.join(jsonDir,f),outDir)
def usage():
    print('Download a given reddit photoshop battle dataset from reference json files')
    print('python2 DownloadRedditDataset.py <json folder> -outputDir <output folder>')
args = sys.argv[1:]
outputDir = '.'
jsonDir = None
while args:
    a = args.pop(0)
    if a == '-h':
        usage()
    elif a == '-outputDir':
        outputDir = args.pop(0)
    elif not jsonDir:
        jsonDir = a
downloadImagesforAllJsons(jsonDir,outputDir)