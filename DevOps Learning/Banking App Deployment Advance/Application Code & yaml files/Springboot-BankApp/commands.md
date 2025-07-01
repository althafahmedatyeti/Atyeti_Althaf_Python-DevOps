## Install Docker 
```sh
sudo apt update
sudo apt install unzip docker.io docker-compose -y
sudo usermod -aG docker $USER && newgrp docker
```

## Install AWSCLI
```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Configure Your AWS Credentials
```sh
aws configure
```

## Install Kubectl
```sh
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl  
chmod +x ./kubectl  
sudo mv ./kubectl /usr/local/bin  
kubectl version --short --client
```

## Install eksctl
```sh
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp  
sudo mv /tmp/eksctl /usr/local/bin  
eksctl version
```

## Create the Cluster
```sh
eksctl create cluster --name=bankapp \
                      --region=us-east-1 \
                      --version=1.30 \
                      --without-nodegroup
```

## OIDC Provider
```sh
eksctl utils associate-iam-oidc-provider \
  --region us-east-1 \
  --cluster bankapp \
  --approve
```


## Create Node Group
```sh
eksctl create nodegroup --cluster=bankapp \
                        --region=us-east-1 \
                        --name=bankapp \
                        --node-type=t2.medium \
                        --nodes=2 \
                        --nodes-min=2 \
                        --nodes-max=2 \
                        --node-volume-size=29 \
                        --ssh-access \
                        --ssh-public-key=default-ec2
```

## Update KubeConfig
`aws eks update-kubeconfig --region us-east-1 --name bankapp`

## ARGOCD Password
`kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo`

## Delete Cluster
`eksctl delete cluster --name=bankapp --region=us-east-1`
