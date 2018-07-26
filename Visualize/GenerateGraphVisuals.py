import os
import sys
import json
import urllib2
import shutil

DatasetName = ""


def usage():
    print("Usage: python GenerateGraphFromJSON.py <json file>")


def generateProvenanceGraph(DatasetName, useNist, ServerAddress, serverDict, jsonFile, outputName):
    buildGraphPage(DatasetName, useNist, ServerAddress, serverDict, jsonFile, outputName)


def generateHeadPortion(title):
    headString = "\
<!DOCTYPE html>\n\
<html>\n\
<head>\n \
<style type=\"text/css\">\n\
body { \n\
  font: 14px helvetica neue, helvetica, arial, sans-serif;\n\
}\n\
    \n\
#cy {\n\
  height: 100%;\n\
  width: 100%;\n\
  position: absolute;\n\
  left: 0;\n\
  top: 0;\n\
}\n\
    \n\
#eat {\n\
  position: absolute;\n\
  left: 1em;\n\
  top: 1em;\n\
  font-size: 1em;\n\
  z-index: -1;\n\
  color: #c88;\n\
}\n\
*{box-sizing: border-box;}\n\
\n\
.img-comp-container{\n\
    position: relative;\n\
    height: 200px; \n\
    width: 400px;\n\
}\n\
\n\
.img-comp-img{\n\
    position: absolute;\n\
    width: auto;\n\
    height: auto;\n\
    overflow: hidden;\n\
}\n\
\n\
.img-comp-img img{\n\
    display: block;\n\
    vertical-align: middle;\n\
}\n\
\n\
.img-comp-slider{\n\
    position: absolute;\n\
    z-index: 9;\n\
    cursor: ew-resize;\n\
    width: 40px;\n\
    height: 40px;\n\
    background-color: #2196F3;\n\
    opacity: 0.7;\n\
    border-radius: 50%;\n\
}\n\
</style>\n\
<meta charset=utf-8 />\n\
<meta name=\"viewport\" content=\"user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, minimal-ui\">\n\
<title>" + "Probe: " + title + "</title>\n\
<link rel=\"stylesheet\" type=\"text/css\" href=\"http://cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.0/jquery.qtip.css\">\n\
<script src=\"http://code.jquery.com/jquery-2.0.3.min.js\"></script>\n\
<script src=\"http://cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.0/jquery.qtip.js\"></script>\n\
<script src=\"https://unpkg.com/cytoscape/dist/cytoscape.min.js\"></script>\n\
<!-- <script src=\"../cytoscape.js/build/cytoscape.js\"></script> --> \n\
<script src=\""+ ServerAddress +":"+ServerPort  +"/cytoscape-qtip.js"+"\"></script>"
    return headString


def generateJSCSS():
    jsCSS = "<script language=\"javascript\">\n\
function initComparisons() {\n\
  var x, i;\n\
  /*find all elements with an \"overlay\" class:*/\n\
  x = document.getElementsByClassName(\"img-comp-overlay\");\n\
  for (i = 0; i < x.length; i++) {\n\
    /*once for each \"overlay\" element: pass the \"overlay\" element as a parameter when executing the compareImages function:*/\n\
    compareImages(x[i]);\n\
  }\n\
  function compareImages(img) {\n\
    var slider, img, clicked = 0, w, h;\n\
    /*get the width and height of the img element*/\n\
    w = img.offsetWidth;\n\
    h = img.offsetHeight;\n\
    /*set the width of the img element to 50%:*/\n\
    img.style.width = (w / 2) + \"px\";\n\
    /*create slider:*/\n\
    slider = document.createElement(\"DIV\");\n\
    slider.setAttribute(\"class\", \"img-comp-slider\");\n\
    /*insert slider*/\n\
    img.parentElement.insertBefore(slider, img);\n\
    /*position the slider in the middle:*/\n\
    slider.style.top = (h / 2) - (slider.offsetHeight / 2) + \"px\";\n\
    slider.style.left = (w / 2) - (slider.offsetWidth / 2) + \"px\";\n\
    /*execute a function when the mouse button is pressed:*/\n\
    slider.addEventListener(\"mousedown\", slideReady);\n\
    /*and another function when the mouse button is released:*/\n\
    window.addEventListener(\"mouseup\", slideFinish);\n\
    /*or touched (for touch screens:*/\n\
    slider.addEventListener(\"touchstart\", slideReady);\n\
     /*and released (for touch screens:*/\n\
    window.addEventListener(\"touchstop\", slideFinish);\n\
    function slideReady(e) {\n\
      /*prevent any other actions that may occur when moving over the image:*/\n\
      e.preventDefault();\n\
      /*the slider is now clicked and ready to move:*/\n\
      clicked = 1;\n\
      /*execute a function when the slider is moved:*/\n\
      window.addEventListener(\"mousemove\", slideMove);\n\
      window.addEventListener(\"touchmove\", slideMove);\n\
    }\n\
    function slideFinish() {\n\
      /*the slider is no longer clicked:*/\n\
      clicked = 0;\n\
    }\n\
    function slideMove(e) {\n\
      var pos;\n\
      /*if the slider is no longer clicked, exit this function:*/\n\
      if (clicked == 0) return false;\n\
      /*get the cursor's x position:*/\n\
      pos = getCursorPos(e)\n\
      /*prevent the slider from being positioned outside the image:*/\n\
      if (pos < 0) pos = 0;\n\
      if (pos > w) pos = w;\n\
      /*execute a function that will resize the overlay image according to the cursor:*/\n\
      slide(pos);\n\
    }\n\
    function getCursorPos(e) {\n\
      var a, x = 0;\n\
      e = e || window.event;\n\
      /*get the x positions of the image:*/\n\
      a = img.getBoundingClientRect();\n\
      /*calculate the cursor's x coordinate, relative to the image:*/\n\
      x = e.pageX - a.left;\n\
      /*consider any page scrolling:*/\n\
      x = x - window.pageXOffset;\n\
      return x;\n\
    }\n\
    function slide(x) {\n\
      /*resize the image:*/\n\
      img.style.width = x + \"px\";\n\
      /*position the slider:*/\n\
      slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + \"px\";\n\
    }\n\
  }\n\
}\n\
$(function(){ // on dom ready\n\
\n\
// photos from flickr with creative commons license\n\
  \n\
var cy = cytoscape({\n\
  container: document.getElementById('cy'),\n\
  \n\
  boxSelectionEnabled: false,\n\
  autounselectify: true,\n\
  \n\
  style: cytoscape.stylesheet()\n\
    .selector('node')\n\
      .css({\n\
        'content': 'data(id)',\n\
        'text-opacity': 0.5,\n\
        'text-valign': 'bottom',\n\
        'text-halign': 'center',\n\
        'font-size': 10,\n\
        'height': 80,\n\
        'width': 80,\n\
        'background-fit': 'cover',\n\
        'border-color': '#000',\n\
        'border-width': 3,\n\
        'border-opacity': 0.5,\n\
        'background-image': 'data(href)',\n\
        'shape':'rectangle'\n\
      })\n\
    .selector('.eating')\n\
      .css({\n\
        'border-color': 'red'\n\
      })\n\
    .selector('.eater')\n\
      .css({\n\
        'border-width': 9\n\
      })\n\
    .selector('edge')\n\
      .css({\n\
        'label': 'data(weight)',\n\
        'edge-text-rotation': 'autorotate',\n\
        'width': 'mapData(normweight, 0, 1, 3, 9)',\n\
        'target-arrow-shape': 'triangle',\n\
        'line-color': '#ffaaaa',\n\
        'target-arrow-color': '#ffaaaa',\n\
        'curve-style': 'bezier'\n\
      })\n"
    return jsCSS


def generateJSEnd():
    jsEnd = "}); // cy init\n\
  \n\
cy.on('tap', 'node', function(){\n\
try { // your browser may block popups\n\
window.open(this.data('href'));\n\
} catch(e)\n\
{ // fall back on url change\n\
window.location.href = this.data('href');\n\
}\n\
}); \n\
\n\
cy.on('tap', 'edge', function(){\n\
    initComparisons();\n\
\n\
});\n\
cy.edges().qtip({\n\
content: function()\n\
{\n\
    srcNode = cy.nodes(\"[id = '\" + this.data('source') + \"']\")\n\
dstNode = cy.nodes(\"[id = '\" + this.data('target') + \"']\")\n\
comparisonString = \"<div class=\\\"img-comp-container\\\"><div class=\\\"img-comp-img\\\"><img src=\\\"\" + srcNode.data('href') + \"\\\" width=\\\"260\\\" height=\\\"180\\\"></div><div class=\\\"img-comp-img img-comp-overlay\\\"><img src=\\\"\" + dstNode.data('href') + \"\\\" width=\\\"260\\\" height=\\\"180\\\"></div></div>\"\n\
return comparisonString},\n\
position: {\n\
my: 'bottom center',\n\
at: 'bottom center'\n\
},\n\
style: {\n\
classes: 'qtip-bootstrap',\n\
tip: {\n\
    width: 260,\n\
    height: 50\n\
}\n\
}\n\
});\n\
}); // on dom ready\n\
</script>\n"
    return jsEnd


def generateHTMLEnd():
    htmlEnd = "</head>\n\
<body>\n\
<div id=\"cy\"></div>\n\
</body>\n\
</html>"
    return htmlEnd


def createSelector(filename, idnum, serverDict, DatasetName):
    filename = getFullFilePath(filename, serverDict)
    selectorString = "\
    .selector('#" + idnum + "')\n\
      .css({\n\
        'background-image': '" + ServerAddress + ":" + ServerPort + "/" + os.path.join(DatasetName, filename) + "'\n\
      })"
    return selectorString


def getFullFilePath(filename, serverDict):
    filename = os.path.basename(filename)
    if serverDict:
        # try:
        fileID = filename.split('.')[0]
        if fileID in serverDict:
            fileloc = os.path.dirname(serverDict[fileID].split(DatasetName)[1]+'/')
        elif filename in serverDict:
            fileloc = os.path.dirname(serverDict[filename].split(DatasetName)[1]+'/')
        else:
            fileloc = ""
        # print(fileloc)
        filename = os.path.join(fileloc, filename)
        # except:
        #     print('no server dict')
        #     pass
    if filename.startswith('/'):
        filename = filename[1:]
    return filename


def generateNodes(jsondict, serverDict, DatasetName):
    allNodes = jsondict["nodes"]
    elementString = "elements: {\n\
    nodes: [\n"
    for i in range(0, len(allNodes)):
        node = allNodes[i]
        filename = getFullFilePath(node['file'], serverDict)

        if useNist:
            idstr = node['id'][2:]
        else:
            idstr = str(i)
        elementString += "{ data: { id: '" + idstr + "', href: '" + ServerAddress + ":"+ ServerPort+"/" + os.path.join(
            DatasetName, filename) + "' } }"
        if i < len(allNodes) - 1:
            elementString += ","
        elementString += "\n"
    elementString += "],\n"
    return elementString


def generateEdges(jsondict, idToNameMap):
    allEdges = jsondict["links"]
    elementString = " edges: [\n"
    for i in range(0, len(allEdges)):
        edge = allEdges[i]
        # sourceNode = os.path.basename(jsondict['nodes'][edge['source']])
        # targetNode = os.path.basename(sjondict['nodes'][edge['target']])
        normWeightweight = edge['normalizedScore']
        weight = '1'
        if 'relationshipConfidenceScore' in edge:
            weight = str(edge["relationshipConfidenceScore"])
        elementString += "{ data: {normweight: " + str(normWeightweight) + ", weight: " + str(
            weight) + ", source: '" + str(edge['source']) + "', target: '" + str(edge['target']) + "' } }"
        if i < len(allEdges) - 1:
            elementString += ","
        elementString += "\n"
    elementString += " ]\n },\n" \
                     "layout: {\n\
                       name: 'breadthfirst',\n\
                       directed: true,\n\
                       padding: 0,\n\
                       spacingFactor: 0\n\
                     }"
    return elementString


def generateJSPortion(jsonDict, idToNameMap, serverDict, DatasetName):
    selectors = []
    # for i in range(0, len(jsonDict['nodes'])):
    #     node = jsonDict['nodes'][i]
    #     selectors.append(createSelector(node["file"], str(i), serverDict, DatasetName))
    elements = generateNodes(jsonDict, serverDict, DatasetName) + generateEdges(jsonDict, idToNameMap)
    jsString = generateJSCSS() + "\n".join(selectors) + ",\n" + elements + generateJSEnd()
    return jsString


def buildGraphPage(DatasetName, useNist, ServerAddress, serverDict, jsonFile, outputName):
    with open(jsonFile, 'r') as fp:
        graphDictionary = json.load(fp)
    idToNameMap = {}
    for n in graphDictionary["nodes"]:
        idToNameMap[n["id"][2:]] = n
    edgeWeights = []
    for e in graphDictionary["links"]:
        conf = 1
        if 'relationshipConfidenceScore' in e:
            conf = e['relationshipConfidenceScore']
        edgeWeights.append(conf)
    minWeight = 0
    maxWeight = 1
    if len(edgeWeights) > 0:
        minWeight = min(edgeWeights)
        maxWeight = max(edgeWeights)
    denom = maxWeight - minWeight
    if denom == 0:
        denom = 1
    for e in graphDictionary["links"]:
        if 'relationshipConfidenceScore' in e:
            e['normalizedScore'] = (e['relationshipConfidenceScore'] - minWeight) / denom
        else:
            e['normalizedScore'] = 1
    graphHTMLString = generateHeadPortion(os.path.basename(jsonFile)) + generateJSPortion(graphDictionary,
                                                                                          idToNameMap, serverDict,
                                                                                          DatasetName) + generateHTMLEnd()
    print("writing " + outputName)
    with open(outputName, "w") as text_file:
        text_file.write(graphHTMLString)


def getJsonFromURL(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jfile = json.loads(f.read())
    return jfile


if __name__ == "__main__":
    useNist = False
    dataset_type = None
    DatasetName = ""
    dir = True
    jsonFile = None
    outputDir = None
    args = sys.argv[1:]
    ServerAddress = None
    ServerPort = None
    while args:
        a = args.pop(0)
        if a == '-h':
            usage()
        elif a == "-outputDir":
            outputDir = args.pop(0)
        elif a == "-server":
            ServerAddress = args.pop(0)
        elif a == "-port":
            ServerPort = args.pop(0)
        elif not jsonFile:
            jsonFile = os.path.join(a,'Data')

        else:
            print("argument %s unknown" % a)
            sys.exit(1)
    if outputDir is None:
        outputDir = os.path.join(jsonFile,'..','Visuals')
    if outputDir is not None:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
    if not ServerPort:
        ServerPort = "8000"
    serverDict = {}
    ServerAddress = 'http://localhost'
    if jsonFile:
        if dir:
            directory = jsonFile
            files = []
            filesToRoots = {}
            for root, dirs, dfiles in os.walk(directory):
                for f in dfiles:
                    if f.endswith('.json'):
                        files.append(os.path.join(root,f))
                        filesToRoots[f] = os.path.basename(os.path.normpath(root))
            if os.path.exists('cytoscape-qtip.js'):
                shutil.copy('cytoscape-qtip.js',os.path.join(outputDir,'..','cytoscape-qtip.js'))
            elif os.path.exists('Visualize/cytoscape-qtip.js'):
                shutil.copy('Visualize/cytoscape-qtip.js',os.path.join(outputDir,'..','cytoscape-qtip.js'))
            else:
                shutil.copy('../cytoscape-qtip.js', os.path.join(outputDir, '..', 'cytoscape-qtip.js'))
            if os.path.exists('cytoscape.min.js'):
                shutil.copy('cytoscape.min.js',os.path.join(outputDir,'..','cytoscape.min.js'))
            elif os.path.exists('Visualize/cytoscape.min.js'):
                shutil.copy('Visualize/cytoscape.min.js',os.path.join(outputDir,'..','cytoscape.min.js'))
            else:
                shutil.copy('../cytoscape.min.js', os.path.join(outputDir, '..', 'cytoscape.min.js'))

            for jsonFile in files:
                if jsonFile.endswith('.json'):

                    outputName = os.path.basename(jsonFile).split(".")[0] + ".html"
                    fullRelativePath = os.path.relpath(os.path.dirname(jsonFile),os.path.abspath(outputDir))
                    if outputDir is not None:
                        outputName = os.path.join(outputDir,outputName)
                        DatasetName = ""
                    generateProvenanceGraph(os.path.join('Data',filesToRoots[os.path.basename(jsonFile)]), useNist, ServerAddress, serverDict, jsonFile, outputName)
        else:
            outputName = os.path.basename(jsonFile).split(".")[0] + ".html"
            if outputDir is not None:
                outputName = os.path.join(outputDir, outputName)
            generateProvenanceGraph(DatasetName, useNist, ServerAddress, serverDict, jsonFile, outputName)
            # buildGraphPage(jsonFile,outputName)
    else:
        print("Usage: python GenerateGraphFromJSON.py <json file> -datasetname <name_of_dataset>")
