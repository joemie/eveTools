import urllib2
import datetime
import os
from xml.dom import minidom

def getValue(str):
  return str[str.find('>')+1:str.find('/')-1]

def getIdDict(file):
  ret = {}
  for line in open(file, 'r+'):
    temp = line.split('~')
    ret[temp[0].strip()] = temp[1].strip()
  return ret
	
def getItemIds(itemDict, fileName):
  ret = []
  for line in open(fileName, 'r+'):
    for key, val in itemDict.iteritems():
	  if val == line.strip():
	    ret.append(key)
  return ret
  
def writeFile(name, orderDict, itemDict):
  date = datetime.datetime.now()
  histFile = open(os.path.join("hist", name + str(date.year) + str(date.month) + str(date.day) + ".csv"), "w+")
  outFile = open(os.path.join("out", name + ".csv"), 'w+')
  outFile.write('item,average,quantity\n')	
  histFile.write('item,average,quantity\n')	
  for item in orderDict:
    outStr = itemDict[item]
    list = orderDict[item]
    for t in list:
      outStr = outStr + ',' + t
    outFile.write(outStr + '\n')
    histFile.write(outStr + '\n')
def fetchMarketData(itemIds, regionIds):
  ret = []
  url = 'http://api.eve-central.com/api/marketstat?'
  typeStr =''
  for id in itemIds:
    typeStr = typeStr + 'typeid=' + str(id) + '&'
  url = url + typeStr + 'regionlimit=10000002'
  #print url
  response = urllib2.urlopen(url)
  out = open('temp.xml', 'w+')
  out.write(response.read())
  out.close()
  xmldoc = minidom.parse('temp.xml')
  reflist = xmldoc.getElementsByTagName('type')
  itemBuyDict = {}
  itemSellDict = {}

  for ref in reflist:
    id = ref.getAttribute('id')
    for buyObj in ref.getElementsByTagName('buy'):
      volStr = getValue(buyObj.getElementsByTagName('volume').item(0).toxml())
      avgStr = getValue(buyObj.getElementsByTagName('avg').item(0).toxml())
      itemBuyDict[id] = [avgStr, volStr]
    for sellObj in ref.getElementsByTagName('sell'):
      volStr = getValue(sellObj.getElementsByTagName('volume').item(0).toxml())
      avgStr = getValue(sellObj.getElementsByTagName('avg').item(0).toxml())
      itemSellDict[id] = [avgStr, volStr] 
  ret.append(itemBuyDict)
  ret.append(itemSellDict)
  return ret
  
masterIdDict = getIdDict('typeId.txt')
mineralTypes = getItemIds(masterIdDict, 'mineralList.txt')
tempList = fetchMarketData(mineralTypes, 10000002)
mineralBuyDict = tempList[0]
mineralSellDict = tempList[1]

writeFile('mineralBuy', mineralBuyDict, masterIdDict)
writeFile('mineralSell', mineralSellDict, masterIdDict)

  
