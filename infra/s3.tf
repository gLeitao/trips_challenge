################################################
# Job Glue Script bucket
################################################
resource "aws_s3_bucket" "s3_glue_job_bucket" {
  bucket = "glue-job-etl-scripts"
}

resource "aws_s3_bucket_acl" "s3_glue_job_bucket_acl" {
  bucket = aws_s3_bucket.s3_glue_job_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "s3_glue_job_bucket_public_access" {
  bucket = aws_s3_bucket.s3_glue_job_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "upload-glue-script" {
  bucket = aws_s3_bucket.s3_glue_job_bucket.id
  key = "scripts/glue/move_raw.py"
  source = "../scripts/glue/move_raw.py"
}

resource "aws_s3_object" "upload-glue-script-dimregions" {
  bucket = aws_s3_bucket.s3_glue_job_bucket.id
  key = "scripts/glue/dimregions.py"
  source = "../scripts/glue/dimregions.py"
}

resource "aws_s3_object" "upload-glue-script-dimdatasources" {
  bucket = aws_s3_bucket.s3_glue_job_bucket.id
  key = "scripts/glue/dimdatasources.py"
  source = "../scripts/glue/dimdatasources.py"
}

resource "aws_s3_object" "upload-glue-script-facttrips" {
  bucket = aws_s3_bucket.s3_glue_job_bucket.id
  key = "scripts/glue/facttrips.py"
  source = "../scripts/glue/facttrips.py"
}

################################################
# Datalake bucket
################################################

resource "aws_s3_bucket" "s3_datalake_bucket" {
  bucket = "trips-datalake"
}

resource "aws_s3_bucket_acl" "s3_datalake_bucket_acl" {
  bucket = aws_s3_bucket.s3_datalake_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "s3_datalake_bucket_public_access" {
  bucket = aws_s3_bucket.s3_datalake_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}