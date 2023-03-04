resource "aws_glue_job" "raw_job" {
  name = "raw_job"
  role_arn = aws_iam_role.glue_role.arn
  glue_version = "3.0" 
  worker_type = "G.1X"
  number_of_workers = 10
  timeout = 2880
  execution_class = "STANDARD"
  max_retries = "1"

  connections = [aws_glue_connection.glue_redsfhit_connection.name]

  command {
    name = "glueetl"
    script_location = "s3://${aws_s3_bucket.s3_glue_job_bucket.id}/scripts/glue/move_raw.py"
    python_version = "3"
  }

  default_arguments = {
    "--enable-metrics" = "true"
    "--enable-spark-ui" = "true"
    "--spark-event-logs-path" = "s3://aws-glue-assets-021380080893-us-east-2/sparkHistoryLogs/"
    "--enable-job-insights" = "true"
    "--enable-glue-datacatalog" = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--job-bookmark-option" = "job-bookmark-disable"
    "--datalake-formats" = "delta"
    "--job-language" = "python"
    "--TempDir" = "s3://aws-glue-assets-021380080893-us-east-2/temporary/"
    "--packages" = "io.delta.sql.DeltaSparkSessionExtension"
  }

  execution_property {
    max_concurrent_runs = 2
  }
  
}


############################################


resource "aws_glue_job" "dimregions_job" {
  name = "dimregions_job"
  role_arn = aws_iam_role.glue_role.arn
  glue_version = "3.0" 
  worker_type = "G.1X"
  number_of_workers = 10
  timeout = 2880
  execution_class = "STANDARD"
  max_retries = "1"

  connections = [aws_glue_connection.glue_redsfhit_connection.name]
  
  command {
    name = "glueetl"
    script_location = "s3://${aws_s3_bucket.s3_glue_job_bucket.id}/scripts/glue/dimregions.py"
    python_version = "3"
  }

  default_arguments = {
    "--enable-metrics" = "true"
    "--enable-spark-ui" = "true"
    "--spark-event-logs-path" = "s3://aws-glue-assets-021380080893-us-east-2/sparkHistoryLogs/"
    "--enable-job-insights" = "true"
    "--enable-glue-datacatalog" = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--job-bookmark-option" = "job-bookmark-disable"
    "--datalake-formats" = "delta"
    "--job-language" = "python"
    "--TempDir" = "s3://aws-glue-assets-021380080893-us-east-2/temporary/"
    "--packages" = "io.delta.sql.DeltaSparkSessionExtension"
  }

  execution_property {
    max_concurrent_runs = 2
  }
  
}


############################################


resource "aws_glue_job" "dimdatasources_job" {
  name = "dimdatasources_job"
  role_arn = aws_iam_role.glue_role.arn
  glue_version = "3.0" 
  worker_type = "G.1X"
  number_of_workers = 10
  timeout = 2880
  execution_class = "STANDARD"
  max_retries = "1"

  connections = [aws_glue_connection.glue_redsfhit_connection.name]
  
  command {
    name = "glueetl"
    script_location = "s3://${aws_s3_bucket.s3_glue_job_bucket.id}/scripts/glue/dimdatasources.py"
    python_version = "3"
  }

  default_arguments = {
    "--enable-metrics" = "true"
    "--enable-spark-ui" = "true"
    "--spark-event-logs-path" = "s3://aws-glue-assets-021380080893-us-east-2/sparkHistoryLogs/"
    "--enable-job-insights" = "true"
    "--enable-glue-datacatalog" = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--job-bookmark-option" = "job-bookmark-disable"
    "--datalake-formats" = "delta"
    "--job-language" = "python"
    "--TempDir" = "s3://aws-glue-assets-021380080893-us-east-2/temporary/"
    "--packages" = "io.delta.sql.DeltaSparkSessionExtension"
  }

  execution_property {
    max_concurrent_runs = 2
  }
  
}

############################################


resource "aws_glue_job" "facttrips_job" {
  name = "facttrips_job"
  role_arn = aws_iam_role.glue_role.arn
  glue_version = "3.0" 
  worker_type = "G.1X"
  number_of_workers = 10
  timeout = 2880
  execution_class = "STANDARD"
  max_retries = "1"

  connections = [aws_glue_connection.glue_redsfhit_connection.name]
  
  command {
    name = "glueetl"
    script_location = "s3://${aws_s3_bucket.s3_glue_job_bucket.id}/scripts/glue/facttrips.py"
    python_version = "3"
  }

  default_arguments = {
    "--enable-metrics" = "true"
    "--enable-spark-ui" = "true"
    "--spark-event-logs-path" = "s3://aws-glue-assets-021380080893-us-east-2/sparkHistoryLogs/"
    "--enable-job-insights" = "true"
    "--enable-glue-datacatalog" = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--job-bookmark-option" = "job-bookmark-disable"
    "--datalake-formats" = "delta"
    "--job-language" = "python"
    "--TempDir" = "s3://aws-glue-assets-021380080893-us-east-2/temporary/"
    "--packages" = "io.delta.sql.DeltaSparkSessionExtension"
  }

  execution_property {
    max_concurrent_runs = 2
  }
  
}