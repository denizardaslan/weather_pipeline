import boto3
from io import StringIO


def save_to_s3(df, bucket_name, file_name):
    # Convert DataFrame to CSV in memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3 = boto3.client("s3")

    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())
        print(f"File {file_name} uploaded to S3 bucket {bucket_name}.")
    except boto3.exceptions.S3UploadFailedError as e:
        print(f"Upload failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
