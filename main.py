from src.extract import extract
from src.transform import transform
from src.load import load
from src.s3_upload import save_to_s3

if __name__ == "__main__":
    # extract()
    df = transform()
    load(df)

    # Save processed data to AWS S3
    bucket_name = "your-s3-bucket-name"
    file_name = "processed_weather_data.csv"
    # save_to_s3(df, bucket_name, file_name)
