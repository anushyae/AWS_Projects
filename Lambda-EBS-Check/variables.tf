variable "aws_region" {
    description = "AWS region where EBS volume will be created"
    type = string
    default = "us-east-1"
  
}

variable "availability_zone" {
    description = "Availability zone to create the EBS volume in"
    type        = string
    default     = "us-east-1a"
}

variable "type" {
    description = "type of the volume"
    type = string
    default = "gp2"
}

variable "size" {
    description = "size of the EBS volume"
    type = number
    default = 8  
}
