output "public_ip" {
  value       = aws_instance.taskflow_server.public_ip
  description = "Public IP of TaskFlow server"
}

output "app_url" {
  value       = "http://${aws_instance.taskflow_server.public_ip}:5000"
  description = "TaskFlow app URL"
}