output "ebs_volume_id" {
    description = "The ID of the created EBS volume"
    value       = aws_ebs_volume.test_volume.id
}

output "ebs_volume_type" {
    description = "The type of the created EBS volume"
    value       = aws_ebs_volume.test_volume.type
}
