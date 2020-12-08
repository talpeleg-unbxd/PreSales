
import os
#	Site variables Here
#
siteKey='ss-unbxd-PetFlow-v18781606272808'
secretKey='379b645399c82a120efee51986748bf4'
# 
#	Name of your feed file
#
#originalFile='./sample.csv'
originalFile='./petflow_variants.csv'
#
#	Below are the mandatory fields that make feed needs (unique & path), 
# 	image there is to make sure you can see the products for console demo
#
mandatories={
	'parent_product_id':'uniqueId',
	'product_title':'title',
	'image_url':'imageUrl'
           }

# These are feilds that should be Multi Value in Schema Later
multiValues = [
	'special_conditions',
	'color',
	'allergic_to',
	'lifestages',
	'breed_sizes',
	'features',
	'types',
	'breadcrumbs_Merge',
	'product_groups',
	'hot_deals']

# These are the fields thatneeds to mapped as variants
vHeaders={
	'id':'variantId',
	'retail_price':'vRetail_price',
	'Quantity':'vQuantity',
	'inventory':'vInventory',

}
#
#   The following fields are optional, helpful for console merechndising demo.
#   Any fields not declared here will be given a text classification
#
mappings={
			'sDecimal':['shipping_length','retail_price','shipping_width',
			'shipping_height','avg_rating','shipping_cost','msrp','gross_margin'], 				# example ['price','rating']
			'sNumber':['num_reviews','vInventory','discount','vQuantity'],							# example ['quantity']
			'sSku':['uniqueId'],						# example ['product_id','manufacturer_sku']
			'sLink':['imageUrl','link','url'],						# example ['url','imageUrl']
			'sAutoSuggest':['title'],					# example ['display_name']
			'sPath':['categoryPath','breadcrumbs_Merge'],					# example ['categoryPath']
			'sBool':[]						# example ['availability','onSale']
		}
#
# Main code begins here 
#
# Importing necessary libraries
#

import presales
import os
import json

#
#creating feed object
#
feed=presales.csvUnbxdFeed(originalFile,mappings,mandatories,vHeaders,multiValues)

#
# execute code for creating schema file
#
def createSchemaFile(siteKey):
	schemaFileName='./files/schema'+siteKey+'.json'
	exportSchema={"feed":{"catalog":{"schema":feed.schema}}}
	f = open(schemaFileName,"w")
	f.write(json.dumps(exportSchema, indent=4,sort_keys=True))
	f.close()
	print ('\nTotal Schema Items\n')
	print (len(feed.schema))
	print('\n\n')
	return schemaFileName

#
# execute code for creating feed file
#
def CreateFeedFile(siteKey):
	exportFeed={"feed":{"catalog":{"add":{"items":feed.items}}}}
	feedFileName='./files/feed'+siteKey+'.json'
	f = open(feedFileName,"w")
	f.write(json.dumps(exportFeed, indent=4,sort_keys=True))
	f.close()
	print ('\nTotal feed Items\n')
	print (len(feed.items))
	print('\n\n')
	return feedFileName


#
# Posting Schema file to unbxd
#
# schemaFileName='./gruntStyle/schema'+siteKey+'.json'
# feedFileName='./gruntStyle/feed'+siteKey+'.json'


myCmd='curl -vX POST \'http://feed-anz.unbxd.io/api/'+siteKey+'/upload/schema\' -H \'Authorization:'+secretKey+'\' -F file=@'+createSchemaFile(siteKey)
print(myCmd)
os.system(myCmd)


#
# Posting feed file to unbxd
#
feedCmd='curl -vX POST \'http://feed-anz.unbxd.io/api/'+siteKey+'/upload/catalog/full\' -H \'Authorization:'+secretKey+'\' -F file=@'+CreateFeedFile(siteKey)
print(feedCmd)
os.system(feedCmd)