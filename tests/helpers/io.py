def save_parquet(df, file_name):
    df.write.option("mapreduce.fileoutputcommitter.algorithm.version", "2").mode('OVERWRITE').parquet(file_name)
