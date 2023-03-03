resource "aws_redshift_cluster" "trips_db_cluster" {
  cluster_identifier = "trips-db"
  database_name      = "dev"
  master_username    = "admin"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible = false
  skip_final_snapshot =  true
}