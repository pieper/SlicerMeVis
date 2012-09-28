import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# MeVisTagVolumeRendering
#

class MeVisTagVolumeRendering:
  def __init__(self, parent):
    parent.title = "MeVisTagVolumeRendering" # TODO make this more human readable by adding spaces
    parent.categories = ["Testing"]
    parent.dependencies = []
    parent.contributors = ["Florian Link (MeVis Medical Systems), Steve Pieper (Isomics)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of connecting 3D Slicer and MeVisLab
    """
    parent.acknowledgementText = """
    This file was originally developed by Florian Link, MMS, and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['MeVisTagVolumeRendering'] = self.runTest

  def runTest(self):
    tester = MeVisTagVolumeRenderingTest()
    tester.runTest()

#
# qMeVisTagVolumeRenderingWidget
#

class MeVisTagVolumeRenderingWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "MeVisTagVolumeRendering Reload"
    self.layout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    self.layout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    # Collapsible button
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    # label map
    self.graySelector = slicer.qMRMLNodeComboBox(parametersCollapsibleButton)
    self.graySelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.graySelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.graySelector.selectNodeUponCreation = False
    self.graySelector.addEnabled = False
    self.graySelector.removeEnabled = False
    self.graySelector.noneEnabled = True
    self.graySelector.showHidden = False
    self.graySelector.showChildNodeTypes = False
    self.graySelector.setMRMLScene( slicer.mrmlScene )
    self.graySelector.setToolTip( "Pick the grayscale volume." )
    parametersFormLayout.addRow("Grayscale", self.graySelector)

    # label map
    self.labelSelector = slicer.qMRMLNodeComboBox(parametersCollapsibleButton)
    self.labelSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.labelSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 1 )
    self.labelSelector.selectNodeUponCreation = False
    self.labelSelector.addEnabled = False
    self.labelSelector.removeEnabled = False
    self.labelSelector.noneEnabled = True
    self.labelSelector.showHidden = False
    self.labelSelector.showChildNodeTypes = False
    self.labelSelector.setMRMLScene( slicer.mrmlScene )
    self.labelSelector.setToolTip( "Pick the target label volume." )
    parametersFormLayout.addRow("Tag LabelMap", self.labelSelector)

    # Add vertical spacer
    self.layout.addStretch(1)

    # apply
    self.applyButton = qt.QPushButton(parametersCollapsibleButton)
    self.applyButton.text = "Apply"
    parametersFormLayout.addWidget(self.applyButton)

    self.applyButton.connect('clicked()', self.onApply)

  def onApply(self):
    grayNode = self.graySelector.currentNode()
    labelNode = self.labelSelector.currentNode()
    if not grayNode and not labelNode:
      qt.QMessageBox.critical(slicer.util.mainWindow(), 'MeVisTagVolumeRendering', "Must select gray volume and label map")
    logic = MeVisTagVolumeRenderingLogic(grayNode, labelNode)
    logic.runMeVis()

  def onReload(self,moduleName="MeVisTagVolumeRendering"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)
    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()

  def onReloadAndTest(self,moduleName="MeVisTagVolumeRendering"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.runTest()

#
# MeVisTagVolumeRenderingLogic
#

class MeVisTagVolumeRenderingLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self,gray,labelMap):
    self.gray = gray
    self.labelMap = labelMap
    self.socket = None
    self.observerTags = []

  def writeVolume(self,volume,name):
    path = slicer.app.temporaryPath + '/%s.nrrd' % name
    s = slicer.vtkMRMLVolumeArchetypeStorageNode()
    s.SetFileName(path)
    s.WriteData(volume)
    return path

  def runMeVis(self):
    path = r"/Applications/MeVisLab.app/Contents/MacOS/MeVisLab"
    grayPath = self.writeVolume(self.gray, 'gray')
    labelPath = self.writeVolume(self.labelMap, 'label')

    for obj,tag in self.observerTags:
      obj.RemoveObserver(tag)
    self.observerTags = []

    tag = self.gray.AddObserver(vtk.vtkCommand.ModifiedEvent, self.reloadVolume)
    self.observerTags.append((self.gray,tag))
    tag = self.labelMap.AddObserver(vtk.vtkCommand.ModifiedEvent, self.reloadVolume)
    self.observerTags.append((self.labelMap,tag))

    args = [path, "-unique", "-diagnosis", "-noide", "-runapp", "SlicerTagVolumeViewer", grayPath, labelPath]
    import subprocess
    print(args)
    env = {'HOME': os.environ['HOME']}
    subprocess.Popen(args,env=env)

  def reloadVolume(self,caller,event):
    if not self.socket:
      self.socket = qt.QTcpSocket()
      self.socket.connectToHost(qt.QHostAddress(qt.QHostAddress.LocalHost), 4949)
    if caller.GetID() == self.gray.GetID():
      self.writeVolume(self.gray, 'gray')
      self.socket.write("reloadGray\n")
      self.socket.waitForBytesWritten()
    if caller.GetID() == self.labelMap.GetID():
      self.writeVolume(self.labelMap, 'label')
      self.socket.write("reloadLabel\n")
      self.socket.waitForBytesWritten()

class MeVisTagVolumeRenderingTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_MeVisTagVolumeRendering1()

  def test_MeVisTagVolumeRendering1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = MeVisTagVolumeRenderingLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
