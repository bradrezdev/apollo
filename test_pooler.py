import socket

regions = [
    "us-east-1", "us-west-1", "us-west-2", "eu-west-1", "eu-west-2", "eu-central-1",
    "ap-southeast-1", "ap-northeast-1", "ap-northeast-2", "sa-east-1", "ca-central-1"
]

for region in regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    try:
        ip = socket.gethostbyname(host)
        print(f"Found {host} -> {ip}")
    except:
        pass
