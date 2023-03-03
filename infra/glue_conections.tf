resource "aws_glue_connection" "glue_redsfhit_connection" {

  name = "glue_redsfhit_connection"
  connection_type = "JDBC"

  connection_properties = {
    JDBC_CONNECTION_URL = "jdbc:redshift://trips-db.cyff0idgfm98.us-east-2.redshift.amazonaws.com:5439/dev"
    PASSWORD            = "" #! removed 
    USERNAME            = "admin"
  }

  physical_connection_requirements {
    availability_zone      = "us-east-2b"
    security_group_id_list = ["sg-0a3653186b7ab5a2e",] 
    subnet_id              = "subnet-0b60abafc70795b2c"
  }

  lifecycle {
    ignore_changes = [
      connection_properties
    ]
  }

}