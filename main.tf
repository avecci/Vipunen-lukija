provider "aws" {
  access_key = "accesskey"
  secret_key = "secretkey"
  region     = "eu-west-1"
}

##############################################################
# Data sources to get VPC, subnets and security group details
##############################################################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = "${data.aws_vpc.default.id}"
}

data "aws_security_group" "default" {
  vpc_id = "${data.aws_vpc.default.id}"
  name   = "default"
}

#####
# DB
#####
module "db" {
    source = "terraform-config/"

  identifier = "vipunendbinstance"

  engine               = "sqlserver-ex"
  major_engine_version = "14.00"
  engine_version       = "14.00.3035.2.v1"
  instance_class       = "db.t2.medium"
  allocated_storage    = 20
  storage_encrypted    = false

  username = "vipunendbadmin"
  password = "YourPwdShouldBeLongAndSecure!"
  port     = "1433"

  vpc_security_group_ids = ["${data.aws_security_group.default.id}"]

  publicly_accessible = true

  # disable backups to create DB faster
  backup_retention_period = 0
  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  tags = {
    Owner       = "vipunenadmin"
    Environment = "rds"
  }

  # DB subnet group
  subnet_ids = ["${data.aws_subnet_ids.all.ids}"]


  create_db_parameter_group = false
  license_model             = "license-included"
  timezone                  = "E. Europe Standard Time"

  # Database Deletion Protection
  deletion_protection = false
}
