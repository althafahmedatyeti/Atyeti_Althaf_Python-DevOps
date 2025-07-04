🚀 Web Application Deployment using Terraform & GitHub Actions (CI/CD)
This project demonstrates an automated CI/CD pipeline to deploy a containerized web application to AWS ECS Fargate using:

Terraform for infrastructure provisioning

GitHub Actions for CI/CD pipeline automation

Amazon ECR for Docker image storage

AWS ECS (Fargate) for container orchestration

Security Groups, Subnets, IAM roles provisioned dynamically

✅ Features
Infrastructure as Code (IaC): All cloud resources (ECR, ECS Cluster, ECS Task, Service, IAM, Security Group, etc.) are provisioned using Terraform.

CI/CD Workflow: GitHub Actions triggers on every push to main, builds a Docker image, pushes it to ECR, and deploys it to ECS.

Secure Deployment: AWS credentials are stored in GitHub Secrets for safe access.

Auto Scaling Ready: The architecture is compatible with Fargate's serverless model for future scalability.

Public Web Access: The deployed container exposes port 5000 to the internet using security group rules.

🧱 Tech Stack
Terraform (v1.6.6)

GitHub Actions

Docker

AWS ECS (Fargate)

AWS ECR

AWS IAM, VPC, Subnets

📁 Repository Structure
plaintext
Copy
Edit
.github/workflows/
  └── deploy.yml         # GitHub Actions CI/CD workflow

terraform/
  ├── main.tf            # Terraform infrastructure definition
  ├── variables.tf       # Input variables
  └── output.tf          # Output values

web-app/
  ├── Dockerfile         # Docker container for web app
  ├── index.html         # Web page content
  └── styles.css         # Styling
