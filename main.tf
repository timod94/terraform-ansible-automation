provider "aws" {
    region = "eu-central-1"  
}

resource "aws_key_pair" "ssh_key" {
    key_name   = "tidos-ssh-key"
    public_key = file("~/.ssh/id_rsa.pub") 
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH access"
  vpc_id      = "vpc-0f98dde3dadf4a22e" 

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2-instance" {
    ami             = "ami-0c8db01b2e8e5298d" # Amazon Linux 2023 AMI
    instance_type   = "t2.micro"
    key_name        = aws_key_pair.ssh_key.key_name # Key Pair korrekt zuweisen
    security_groups = [aws_security_group.allow_ssh.name]
    associate_public_ip_address = true

    tags = {
        Name = "TidosInstance"
    }
}

output "instances" {
    value = [
        {
            ip_address = aws_instance.ec2-instance.public_ip
            username   = "ec2-user"
            key_name   = aws_key_pair.ssh_key.key_name
        }
    ]
}
