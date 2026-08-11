// Single source of truth for whether the accounts layer is wired up.
//
// The whole auth surface follows the same idiom as the live chat box
// (`live-debate.tsx`): it is *dormant* until configured. With the Supabase env
// vars unset, `isSupabaseConfigured` is false, the sign-in UI hides, and the
// session-refresh proxy is a no-op — so the site behaves exactly as it did
// before accounts existed. Shipping this code before the Supabase project
// exists is therefore safe.

export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
export const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const isSupabaseConfigured = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);
