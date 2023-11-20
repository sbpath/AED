import os
import urllib.request
import boto3

def lambda_handler(event, context):
    # GitHub URL of the file you want to download
    github_url = "https://raw.githubusercontent.com/sbpath/AED/main/eol-file.txt"

    # S3 bucket and object key where you want to store the file
    s3_bucket = "aed-618828439365"
    s3_key = "eol-file.txt"

    # Temporary file to store the downloaded content
    temp_file_path = "/tmp/temp_file.txt"

    # Download the file from GitHub using urllib
    try:
        with urllib.request.urlopen(github_url) as response:
            file_content = response.read().decode('utf-8')

        # Save the file content to the temporary file
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(file_content)

        # Upload the file to S3
        s3_client = boto3.client('s3')
        s3_client.upload_file(temp_file_path, s3_bucket, s3_key)

        # Clean up: Remove the temporary file
        os.remove(temp_file_path)

        return {
            'statusCode': 200,
            'body': 'File successfully downloaded from GitHub and uploaded to S3.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
