import requests
import json

def InputFunc():

    print ('input url here')

    url = input()

    r = requests.get(url=url)


    decode_json = json.loads(r.text)

    return decode_json['Obj']


def dealWithData(Obj):



    if isinstance(Obj,list):

        #print ('input is list')

        for key in Obj[0]:
            print ('@property(nonatomic,copy)NSString *' + key + ';')

        newObj = Obj[0]

        dealWithData(newObj)

    else:
        #print ('input is dic')

       # for firstKey in Obj:
        #    print (firstKey)

        print ('input key here')
        inputKeys = input()
        newKey = inputKeys

        newDic= Obj[inputKeys]

        print (newKey)
        if inputKeys == 'goBack':
            dealWithData(Obj)
        else:

            try:
                if isinstance(newDic, dict):

                    for key in newDic:
                        print ('@property(nonatomic,copy)NSString *' + key + ';')

                    dealWithData(Obj[inputKeys])
            except:
                return
                print ('')


        print ('验证2'+newKey)



    # for key in arr[0]:
    #     print ('@property(nonatomic,copy)NSString *'+ key+';')


    # print ('input key here')
    # inputKeys = input()
    #
    # dic1 = arr[0]
    #
    # dic2 = dic1[inputKeys]
    #
    #
    # for key in dic2:
    #     print ('@property(nonatomic,copy)NSString *'+ key+';')






def jsonRep(jsonStr):
    replaceStr = jsonStr.replace('"',r'\"')
    print (replaceStr)



if __name__ == '__main__':
    #jsonStr = input()
    #jsonRep(jsonStr)

    data = InputFunc()

    dealWithData(data)