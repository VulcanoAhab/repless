from custodi.smallBoto import S3Bucket, #Relational

def bucketToSql(Configuration):
    """
    headers | type::manual, biggest, commons
    """
    ## get s3 iterator
    S3Bucket.basic_conn(
        aws_access_key_id=Configuration.aws_key,
        aws_secret_access_key=Configuration.aws_secret,
        region_name=Configuration.region_name
    )
    s3B=S3Bucket(Configuration.bucket_name)
    ## get first object

    ## create table

    ## start saving

        ## if column not in, create column and save