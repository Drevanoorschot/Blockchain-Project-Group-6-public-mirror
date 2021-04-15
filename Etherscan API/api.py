import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json

apiKey = "UT2GWKR7T6PCIMSPE9ZJKMHHUR53TN4XT4"
timestamp = "1578638524"

responseBlockNumber = requests.get("https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp="+timestamp+"&closest=before&apikey="+apiKey)
blockNumber = responseBlockNumber.json()['result']
print(blockNumber)
url = "https://etherscan.io/txs?block="+blockNumber
responseContractsOfBlock = Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
webpage = urlopen(responseContractsOfBlock).read()
soup = BeautifulSoup(webpage, 'html.parser')

# Needed for searching all pages
# print(soup.find_all("strong", class_="font-weight-medium"))

print(soup.find_all("a", class_="hash-tag text-truncate"))

# contractAddress = "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b"
# print("Contract Address:", contractAddress)
#
# responseContractSourceCode = requests.get("https://api.etherscan.io/api?module=contract&action=getsourcecode&address="+contractAddress+"&apikey="+apiKey)
# sourceCode = responseContractSourceCode.json()['result'][0]['SourceCode']
#
# if len(sourceCode) > 1:
#     print(responseContractSourceCode.status_code)
#     print(sourceCode)
# else:
#     print("Contract not verified")