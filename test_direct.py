import psycopg2
url = "postgresql://postgres:qujjeD-nicqow-venza2@aws-0-us-west-2.pooler.supabase.com:5432/postgres"
try:
    print("Testing port 5432 on pooler domain...")
    conn = psycopg2.connect(url, connect_timeout=3)
    print("SUCCESS on port 5432!")
    conn.close()
except Exception as e:
    print(f"FAILED on port 5432: {e}")

url2 = "postgresql://postgres.zwlejtloybqpbotkdanu:qujjeD-nicqow-venza2@aws-0-us-west-2.pooler.supabase.com:5432/postgres"
try:
    print("Testing port 5432 on pooler domain with tenant...")
    conn = psycopg2.connect(url2, connect_timeout=3)
    print("SUCCESS on port 5432 with tenant!")
    conn.close()
except Exception as e:
    print(f"FAILED on port 5432 with tenant: {e}")
