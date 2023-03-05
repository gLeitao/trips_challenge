resource "aws_glue_connection" "glue_redsfhit_connection" {

  name = "glue_redsfhit_connection"
  connection_type = "JDBC"

  connection_properties = {
    JDBC_CONNECTION_URL = var.redshift_jdbc_string
    PASSWORD            = "" #! removed 
    USERNAME            = "admin"
  }

  physical_connection_requirements {
    availability_zone      = var.availability_zone 
    security_group_id_list = var.security_group_id_list 
    subnet_id              = var.subnet_id
  }

  lifecycle {
    ignore_changes = [
      connection_properties
    ]
  }

}