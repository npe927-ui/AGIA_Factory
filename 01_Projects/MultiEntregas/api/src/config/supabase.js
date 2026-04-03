import { createClient } from '@supabase/supabase-js'

if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SECRET_KEY) {
  throw new Error('SUPABASE_URL y SUPABASE_SECRET_KEY son requeridas')
}

// service_role key — acceso completo, solo usar en servidor
export const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY,
  {
    auth: {
      persistSession: false,
      autoRefreshToken: false,
    },
  }
)
