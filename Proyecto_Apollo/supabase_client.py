from supabase import create_client


SUPABASE_URL="https://mqajbtjxwdtwimoavhjz.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xYWpidGp4d2R0d2ltb2F2aGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwNDg4NzUsImV4cCI6MjA2MzYyNDg3NX0.JvgIf5-4Xuxef-bQi6JgFHI0CbdpiOouI654cxqwMQo"
        

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)