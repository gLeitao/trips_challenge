variable "region" {
  description = "Region used into aws account"
  type    = string
  default = "us-east-2"
}

variable "glue_bucket_name" {
  description = "Name of the s3 bucket used to store glue scripts"
  type    = string
  default = "glue-job-etl-scripts"
}

variable "datalake_bucket_name" {
  description = "Name of the s3 bucket used to store transformed data"
  type    = string
  default = "trips-datalake"
}


variable "redshift_jdbc_string" {
  description = "String connection of redshift cluster"
  type    = string
  default = "jdbc:redshift://trips-db.cyff0idgfm98.us-east-2.redshift.amazonaws.com:5439/dev"
}


################################################
# Network variables
################################################
variable "availability_zone" {
  description = "Availability zone of VPC"
  type    = string
  default = "us-east-2b"
}

variable "security_group_id_list" {
  description = "Security group of VPC"
  type    = list(string)
  default = ["sg-0a3653186b7ab5a2e",] 
}

variable "subnet_id" {
  description = "Subnet id of VPC"
  type    = string
  default = "subnet-0b60abafc70795b2c"
}