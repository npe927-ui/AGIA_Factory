-- =====================================================
-- MIGRATION: Add guest client support
-- =====================================================
-- This migration allows clients to be created without a user account
-- for public booking (walk-in clients via QR code)
-- =====================================================

-- 1. Make user_id nullable (for guest clients)
ALTER TABLE clients
ALTER COLUMN user_id DROP NOT NULL;

-- 2. Add fields for guest client information
-- These fields store contact info for clients without accounts
ALTER TABLE clients
ADD COLUMN IF NOT EXISTS full_name TEXT,
ADD COLUMN IF NOT EXISTS email TEXT;

-- 3. Create index for email lookups (for finding existing guest clients)
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email) WHERE email IS NOT NULL;

-- 4. Update RLS policies to allow public booking API to create clients
-- Note: The service role key bypasses RLS, so this may not be needed
-- but adding it for completeness

-- Allow inserting guest clients (no user_id required)
CREATE POLICY IF NOT EXISTS "Allow public guest client creation" ON clients
FOR INSERT
WITH CHECK (user_id IS NULL);

-- Allow selecting clients only if authorized or for exact email matching in booking (SECURED)
CREATE POLICY IF NOT EXISTS "Allow select clients by email" ON clients
FOR SELECT
USING (
  (auth.uid() IS NOT NULL) OR -- Authenticated users (Lawyers/Admins) can see (restricted by their own RLS)
  (id::text = current_setting('request.headers')::json->>'x-client-id') -- Only allow matching if ID is provided
);

-- Verify changes
SELECT column_name, is_nullable, data_type
FROM information_schema.columns
WHERE table_name = 'clients'
AND table_schema = 'public'
ORDER BY ordinal_position;
