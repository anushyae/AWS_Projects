resource "aws_ebs_volume" "test_volume" {
    availability_zone = var.availability_zone
    type = var.type
    size = var.size  
    tags = {
      Name = "Terraform-test-volume"
      Createdby = "Terraform"
      Purpose = "Lambda-EBS-check"
    }
}

