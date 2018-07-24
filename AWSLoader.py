import boto3
import pandas as pd

loader_header = pd.read_csv("loader.csv")

# Create an  clients
s3 = boto3.client('s3',region_name='us-west-1')
lambda_client = boto3.client('lambda',region_name='us-west-1')

fileHeader = loader_header['Files']
bucket_name = '<S3 Bucket Name>'
fn_role = '<I AM Role>'
handlerName = 'createTimer'
environmentSetup = {'string':'string'}


for testFile in fileHeader:
	filename = testFile
	s3.upload_file(filename, bucket_name, filename)
	print("S3 File Updload Completed")
	print("S3 Link : "+ "https://s3.amazonaws.com/<s3bucketname>/"+testFile )

	funcName = testFile.replace(".zip","")


	print(funcName)
	fn_name = "Prefix"+funcName


	# #Delete Lambda Function
	# try:
	# 	response = lambda_client.delete_function(FunctionName=funcName)
	# except:
	# 	print('No Function Exists')
	# 	print("Creating Function")


	try:
		response = lambda_client.create_function(
	    FunctionName=fn_name,
	    Runtime='python2.7',
	    MemorySize = 3008,
	    Timeout = 180,
	    Role=fn_role,
	    Handler="{0}.{1}".format(funcName,handlerName),
	    Environment={'Variables': environmentSetup},
	    Code={'S3Bucket':bucket_name,'S3Key':testFile, })
		print(response)

	except Exception as error:
		print(error)
		print("Updating the Lambda Functions")
		response = lambda_client.update_function_code(
		FunctionName=fn_name,S3Bucket=bucket_name,S3Key=testFile,Publish=True)
		print(response)
	
	
