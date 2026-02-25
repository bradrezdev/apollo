import socket
import sys

# Test if we can even import psycopg2
try:
    import psycopg2
except ImportError:
    print("psycopg2 not installed")
    sys.exit(0)

url = "postgresql://postgres.zwlejtloybqpbotkdanu:qujjeD-nicqow-venza2@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

try:
    print("Connecting...")
    conn = psycopg2.connect(url, connect_timeout=5)
    print("Success!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
