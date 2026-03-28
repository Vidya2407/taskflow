provider "aws" {
  region = var.region
}

# VPC
resource "aws_vpc" "taskflow_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "taskflow-vpc"
  }
}

# Subnet
resource "aws_subnet" "taskflow_subnet" {
  vpc_id                  = aws_vpc.taskflow_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "taskflow-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "taskflow_igw" {
  vpc_id = aws_vpc.taskflow_vpc.id
  tags = {
    Name = "taskflow-igw"
  }
}

# Route Table
resource "aws_route_table" "taskflow_rt" {
  vpc_id = aws_vpc.taskflow_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.taskflow_igw.id
  }
  tags = {
    Name = "taskflow-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "taskflow_rta" {
  subnet_id      = aws_subnet.taskflow_subnet.id
  route_table_id = aws_route_table.taskflow_rt.id
}

# Security Group
resource "aws_security_group" "taskflow_sg" {
  name        = "taskflow-sg"
  description = "Allow web and SSH traffic"
  vpc_id      = aws_vpc.taskflow_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "taskflow-sg"
  }
}

# EC2 Instance
resource "aws_instance" "taskflow_server" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.taskflow_subnet.id
  vpc_security_group_ids = [aws_security_group.taskflow_sg.id]
  key_name               = "taskflow-key"

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    docker pull vidya2407/taskflow:latest
    docker run -d -p 5000:5000 vidya2407/taskflow:latest
  EOF

  tags = {
    Name = "taskflow-server"
  }
}