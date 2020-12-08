import csv
import time

def getTheStuff(id):
    f=open('petflow_product_export.csv','r')
    worker=csv.DictReader(f)
    for i in worker:
        if i['id']==id:
            return i
            f.close()
            break
        else:
            next


def schemaMaker(fieldName,dataType,multiValue,autoSuggest,isVariant):
        output={}
        output["fieldName"]=fieldName
        output["dataType"]=dataType
        if multiValue=='t':
            output["multiValue"]=True
        else:
            output["multiValue"]=False
        if autoSuggest=='t':
            output["autoSuggest"]=True
        else:
            output["autoSuggest"]=False
        if isVariant=='t':
            output["isVariant"]=True
        else:
            output["isVariant"]=False
        return output

def createSchema (headings,mapping):	
        wrapper=[]
        for i in headings:
            shmek=i.replace(' ','_')
            if shmek in mapping["sDecimal"]:
                wrapper.append(schemaMaker(shmek,'decimal','f','f','f'))
            elif shmek in mapping["sSku"]:
                wrapper.append(schemaMaker(shmek,'sku','f','f','f'))
            elif shmek in mapping["sLink"]:
                wrapper.append(schemaMaker(shmek,'link','f','f','f'))
            elif shmek in mapping["sNumber"]:
                wrapper.append(schemaMaker(shmek,'number','f','f','f'))
            elif shmek in mapping["sAutoSuggest"]:
                wrapper.append(schemaMaker(shmek,'text','f','t','f'))
            elif shmek in mapping["sPath"]:
                wrapper.append(schemaMaker(shmek,'path','t','f','f'))
            elif shmek in mapping["sBool"]:
                wrapper.append(schemaMaker(shmek,'bool','f','f','f'))
            else:
                wrapper.append(schemaMaker(shmek,'text','f','f','f'))
        return wrapper

class csvUnbxdFeed:
    def __init__(self, filename,mappings,mandatories,vHeaders,multiValues):
        self.file=filename
        f = open(filename,'r')
        self.work=csv.DictReader(f)
        self.items=[]
        headers =[]
        # Preloading Variant Headers into headers
        for x,y in vHeaders.items():
            headers.append(y)
        
        # products is an array for understing which product ID's
        # have seeen before, easier lookup
        products=[]
        other_fields=['special_conditions','types','product_groups','lifestages','breed_sizes',
        'main_ingredient','features','hot_deals']

        #Now the iteration on file begins
        for row in self.work:
            # If this si a first time we are seeing a new product ID
            if row['parent_product_id'] not in products:
                products.append(row['parent_product_id'])
                if len(products)%100 == 0:
                    named_tuple = time.localtime() # get struct_time
                    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
                    tracker="Reached "+str(len(products))+" results at "+time_string
                    print(tracker)
                record={}
                record['variants']=[]
                vRecord={}
                someotherShit=getTheStuff(row['id'])
                for runner in other_fields:
                    if someotherShit[runner]:
                        if runner in multiValues:
                            record[runner]=someotherShit[runner].split(',')
                        else:
                            record[runner]=someotherShit[runner]
                        if runner not in headers:
                            headers.append(runner)
                for x,y in row.items():
                    if y: #so we dont index empty fields
                        if x in vHeaders:
                            vRecord[vHeaders[x]]=y
                        elif x in mandatories:        #These are the mandatory fields
                            record[mandatories[x]]=y
                            if mandatories[x] not in headers:
                                headers.append(mandatories[x])
                        elif x in multiValues:
                            record[x]=y.split(',')
                            if x not in headers:
                                headers.append(x)
                        else:
                            record[x.replace(':','-').replace(' ','_')]=y.replace('"','') #whatever is left
                            if x.replace(':','-').replace(' ','_') not in headers:
                                headers.append(x.replace(':','-').replace(' ','_'))
                record['variants'].append(vRecord)
                self.items.append(record)
            # Part below understands that a product ID has been created 
            # and therefore just creates a variant entry
            else: 
                vRecord={}
                for x,y in row.items():
                    if y: #so we dont index empty fields
                        if x in vHeaders:
                            vRecord[vHeaders[x]]=y
                for runner in self.items:
                    if runner['uniqueId'] == row['parent_product_id']:
                        runner['variants'].append(vRecord)
                        break
        print()
        #creating Schema Items
        self.schema=createSchema(headers,mappings)
        for i in self.schema:
            if i['fieldName'] in multiValues:
                i['multiValue'] = True
        sVheaders =[]
        for x,y in vHeaders.items():
            sVheaders.append(y)
        for i in self.schema:
            if i['fieldName'] in sVheaders:
                i['isVariant'] = True
        f.close()