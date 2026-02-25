import psycopg2
import sys

regions = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2", 
    "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1",
    "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ap-northeast-2", "ap-south-1",
    "sa-east-1", "ca-central-1", "me-south-1", "af-south-1"
]

for region in regions:
    url = f"postgresql://postgres.zwlejtloybqpbotkdanu:qujjeD-nicqow-venza2@aws-0-{region}.pooler.supabase.com:6543/postgres"
    print(f"Trying {region}...")
    try:
        conn = psycopg2.connect(url, connect_timeout=3)
        print(f"\n=> SUCCESS in region: {region}!")
        conn.close()
        sys.exit(0)
    except Exception as e:
        if "Tenant or user not found" not in str(e):
            print(f"  Unexpected error: {e}")
            pass

print("Not found in any standard region.")
