#----------------------------------------------------------------------------------
#! Macro module SlicerTagVolumeViewer
#/*!
# \file    SlicerTagVolumeViewer.py
# \author  Florian Link
# \date    2012-09-26
#
# 
# */
#----------------------------------------------------------------------------------

from mevis import *

from PythonQt import QtCore
from PythonQt import QtNetwork

server = None
socket = None

def init():
  global server
  server = QtNetwork.QTcpServer()
  print server.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), 4949)
  server.newConnection.connect(newConnection)

def newConnection():
  global socket, server
  socket = server.nextPendingConnection()
  print socket
  socket.readyRead.connect(tryToRead)

def tryToRead():
  global socket
  if not socket.canReadLine():
    return
  command = str(socket.readLine()).strip()
  print(command)
  if command == "reloadLabel":
    ctx.field("tagVolume.close").touch()
    ctx.field("tagVolume.open").touch()
  elif command == "reloadGray":
    ctx.field("volume.close").touch()
    ctx.field("volume.open").touch()
    ctx.field("SoExaminerViewer.viewAll").touch()
  else:
    MLAB.logError("unknown command: %s" % command)

def run(args, path):
  input1  = ""
  input2 = ""
  MLAB.log("run " + str(args))
  MLAB.log("path " + str(path))
  
  if args[0]:
    input1 = MLABFileManager.absPath(args[0], path)
  if args[1]:
    input2 = MLABFileManager.absPath(args[1], path)

  if input1 and input2:
    ctx.field("volume.fileName").value = input1
    ctx.field("tagVolume.fileName").value = input2
    ctx.field("SoExaminerViewer.viewAll").touch()
