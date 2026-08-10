# AUTH-SETUP — turning on accounts (Phase 4A)

The code for accounts (Google, Microsoft, email/password) is **built and merged**,
and follows the same "dormant until configured" idiom as the live chat box: with
the Supabase env vars unset it renders nothing and the site is unchanged. This doc
is the click-by-click guide to the steps that need **your** cloud consoles — they
can't be done from the repo.

Work top to bottom. Rough time: Google ~15 min, Microsoft ~15 min, Supabase
settings ~10 min, Vercel ~5 min.

---

## 0. Your project's constants (copy these; you'll paste them a lot)

| Thing | Value |
|---|---|
| Supabase project | **christisgod** (`qpqlllccyudypgdvtwcx`, region us-east-2) |
| Supabase Project URL | `https://qpqlllccyudypgdvtwcx.supabase.co` |
| **Provider callback URL** (redirect URI) | `https://qpqlllccyudypgdvtwcx.supabase.co/auth/v1/callback` |
| Publishable (anon) key | `sb_publishable_CXu-d6fi__69xGi21qEgsQ_Z1vv_8OG` |
| Production site | `https://christisgod.app` |
| Local dev | `http://localhost:3100` |

**The single most important fact:** every OAuth provider (Google, Microsoft)
redirects back to the **Supabase callback URL** above — *not* to christisgod.app.
The flow is: browser → provider → Supabase (`/auth/v1/callback`) → your app
(`/auth/callback`) → signed in. So the provider consoles only ever need the
Supabase callback URL. Your app origin is registered separately, in Supabase's
own redirect allow-list (§3).

### What's already done (so you don't redo it)
- `public.profiles` table + RLS + `on_auth_user_created` trigger — migration
  `web/supabase/migrations/0001_profiles.sql`, **applied** to the project.
- `web/.env.local` holds the dev URL + publishable key, so `npm run dev` already
  has **email/password** working locally right now. OAuth needs §1–§2 first.

---

## 1. Google — `Continue with Google`

### 1a. Create / pick a Google Cloud project
1. Go to <https://console.cloud.google.com>.
2. Top bar → project picker → **New Project** (or reuse one). Name it e.g.
   `christ-is-god`. Create, then make sure it's the **selected** project.

### 1b. Configure the OAuth consent screen (branding + audience)
Google recently renamed this area to **Google Auth Platform**. Either path works:
- New: left nav → **Google Auth Platform** → **Branding** / **Audience**, or go to
  <https://console.cloud.google.com/auth/overview>.
- Classic: **APIs & Services → OAuth consent screen**.

Steps:
1. **User type / Audience: External.** (Internal only exists for Workspace orgs and
   would restrict sign-in to your org.)
2. **Branding:** App name `Christ Is God`, user support email (yours), app
   logo optional, developer contact email (yours).
3. **Authorized domains** — add both:
   - `supabase.co`
   - `christisgod.app`
4. **Scopes:** the defaults are enough — `openid`, `.../auth/userinfo.email`,
   `.../auth/userinfo.profile`. These are **non-sensitive**, so Google does **not**
   require an app-verification review. Don't add sensitive scopes you don't need.
5. **Publishing status:** set the app to **In production** (Audience page →
   *Publish app*). While it's in *Testing*, only emails you add as *Test users* can
   sign in. With only the basic scopes above, publishing needs no Google review.

### 1c. Create the OAuth client ID
1. **Google Auth Platform → Clients** (or **APIs & Services → Credentials**) →
   **Create client** → **Create OAuth client ID**.
2. **Application type: Web application.** Name it `Supabase — Christ Is God`.
3. **Authorized JavaScript origins** → Add URI:
   ```
   https://qpqlllccyudypgdvtwcx.supabase.co
   ```
4. **Authorized redirect URIs** → Add URI (this is the important one — paste
   exactly, no trailing slash):
   ```
   https://qpqlllccyudypgdvtwcx.supabase.co/auth/v1/callback
   ```
5. **Create.** A dialog shows the **Client ID** and **Client secret** — copy both.

### 1d. Paste into Supabase
1. Supabase Dashboard → your project → **Authentication → Sign In / Providers →
   Google**.
2. Toggle **Enable**. Paste **Client ID** and **Client Secret**.
3. Leave **Authorized Client IDs** blank (that field is for native/one-tap nonce
   flows; the web flow doesn't need it).
4. **Save.**

> Gotcha: `Error 400: redirect_uri_mismatch` at sign-in = the redirect URI in
> step 1c.4 doesn't *exactly* match the callback (watch for `http` vs `https`, a
> trailing slash, or the wrong project ref). Fix it in Google, wait ~1 min.

---

## 2. Microsoft — `Continue with Microsoft` (Azure / Entra ID)

Our sign-in calls this provider as `azure` (Supabase's id for Microsoft). No code
change is needed — only the console config below.

### 2a. Register the application
1. Go to <https://portal.azure.com> → **Microsoft Entra ID** (formerly Azure AD) →
   **App registrations** → **New registration**.
2. **Name:** `Christ Is God`.
3. **Supported account types** — pick based on who should sign in:
   - **Recommended (broadest):** *Accounts in any organizational directory (Any
     Microsoft Entra ID tenant - Multitenant) **and** personal Microsoft accounts
     (e.g. Skype, Xbox)*. This is the "any Microsoft account" option.
   - Single-org only: *Accounts in this organizational directory only* — then you
     **must** set the Tenant URL in step 2d.
4. **Redirect URI:** platform dropdown **Web**, value:
   ```
   https://qpqlllccyudypgdvtwcx.supabase.co/auth/v1/callback
   ```
5. **Register.**

### 2b. Copy the client ID
On the app's **Overview** page, copy **Application (client) ID**.

### 2c. Create a client secret
1. Left nav → **Certificates & secrets → Client secrets → New client secret**.
2. Description `supabase`, expiry (max 24 months — set a calendar reminder to
   rotate before it lapses, or OAuth silently breaks).
3. **Copy the secret `Value` immediately** — it's shown only once. Copy the
   **Value**, *not* the Secret ID (a common mix-up).

### 2d. (Personal accounts) check permissions & claims
1. **API permissions** should list Microsoft Graph delegated `User.Read` by
   default. Add `email`, `openid`, `profile` if not present, then **Grant admin
   consent** if the button is available.
2. This ensures the user's email comes back in the token for personal Microsoft
   accounts too.

### 2e. Paste into Supabase
1. Supabase Dashboard → **Authentication → Sign In / Providers → Azure**.
2. **Enable.** Paste **Application (client) ID** and the secret **Value**.
3. **Azure Tenant URL:**
   - Multitenant + personal accounts → **leave blank** (Supabase uses the
     `common` endpoint).
   - Single-tenant → `https://login.microsoftonline.com/<your-tenant-id>`.
4. **Save.**

> Gotcha: `AADSTS50011: redirect URI … does not match` = the Web redirect URI in
> 2a.4 is off. `AADSTS700016 / app not found in tenant` = you chose single-tenant
> but left the Tenant URL blank (or vice-versa). `AADSTS650051` /email missing =
> do step 2d.

---

## 3. Supabase Auth settings — URLs + email

### 3a. URL configuration (required for redirects to work)
Dashboard → **Authentication → URL Configuration**:
1. **Site URL:** `https://christisgod.app`
2. **Redirect URLs** → add each:
   - `https://christisgod.app/**`
   - `http://localhost:3100/**`
   - *(optional, for Vercel preview deploys)* `https://*.vercel.app/**`

> Why: after a provider authenticates, our app calls back with
> `?next=<path>` and Supabase will only redirect to origins on this allow-list.
> Miss this and OAuth ends on an "invalid redirect" error even though the provider
> succeeded.

### 3b. Custom SMTP (do this before enabling email confirmation in production)
Supabase's **built-in email sender is for testing only** — it's rate-limited to a
few messages per hour and won't reliably deliver signup confirmations to real
users. Before promoting:
1. Pick an SMTP provider and verify your sending domain there (SPF + DKIM DNS
   records). Good options: **Resend**, AWS SES, SendGrid, Postmark, Mailgun.
2. Supabase Dashboard → **Authentication → Emails → SMTP Settings** (a.k.a.
   Project Settings → Auth) → **Enable Custom SMTP**. Fill:
   - Host (e.g. `smtp.resend.com`), Port (`465` SSL or `587` STARTTLS)
   - Username / Password (the provider's SMTP credentials or API key)
   - **Sender email** (must be on your verified domain, e.g.
     `no-reply@christisgod.app`) and **Sender name** (`Christ Is God`).
3. **Authentication → Rate Limits** → raise the email rate now that a real sender
   is behind it.
4. Optionally review **Email Templates** (Confirm signup, Magic Link, Reset
   password) — the confirmation link uses `{{ .ConfirmationURL }}`, which routes
   through Supabase and then to your Site URL, so 3a must be correct first.

### 3c. Email confirmation toggle
Dashboard → **Authentication → Sign In / Providers → Email**:
- For production, keep **Confirm email = ON** (users verify before first sign-in).
- For quick local testing you *may* turn it OFF temporarily — but turn it back on
  before launch.

> Gotcha you already saw: Supabase rejects obviously-fake domains (`example.com`)
> with "Email address is invalid." Test with a real, deliverable address once SMTP
> is set.

---

## 4. Vercel — production env vars + redeploy

The web app lives in the `web/` subdirectory; make sure you're editing the Vercel
project whose **Root Directory** is `web` (per the recent root-directory fix).

1. Vercel Dashboard → your **web** project → **Settings → Environment Variables** →
   add two, scoped to **Production, Preview, and Development**:

   | Key | Value |
   |---|---|
   | `NEXT_PUBLIC_SUPABASE_URL` | `https://qpqlllccyudypgdvtwcx.supabase.co` |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `sb_publishable_CXu-d6fi__69xGi21qEgsQ_Z1vv_8OG` |

2. **Redeploy — this is mandatory, not optional.** `NEXT_PUBLIC_*` vars are inlined
   at **build time**, so an existing deployment won't pick them up. Either push a
   commit, or Vercel → **Deployments → ⋯ → Redeploy** on the latest.
3. After the deploy finishes, the sign-in UI activates automatically (the
   `isSupabaseConfigured` guard now sees the vars).

Both keys are **browser-safe**: the publishable key is public by design, and
**Row-Level Security** is what actually protects data. Do **not** put the service-
role/secret key in any `NEXT_PUBLIC_*` var.

---

## 5. Verify end-to-end

1. **Email/password (works locally today):** `cd web && npm run dev` →
   <http://localhost:3100/sign-in> → *Create an account* with a real address →
   confirm via email (if 3c is on) → sign in. On first signup a `profiles` row is
   auto-created by the trigger.
2. **Google / Microsoft:** on the deployed site (or locally), click each provider
   button → complete the provider prompt → you land back signed in, and the header
   (in the reading view) shows your name + a sign-out control.
3. **Confirm the profile row:** Supabase Dashboard → **Table Editor → profiles** →
   your new user is there with `role = free`.

---

## 6. Troubleshooting quick table

| Symptom | Cause / fix |
|---|---|
| `redirect_uri_mismatch` (Google) | Redirect URI in §1c.4 ≠ the Supabase callback exactly. |
| `AADSTS50011` reply-URL error (MS) | Web redirect URI in §2a.4 wrong. |
| `AADSTS700016` app-not-found (MS) | Account-type vs Tenant URL mismatch (§2a.3 / §2e.3). |
| "Unsupported provider / not enabled" | Provider not toggled on + saved in Supabase (§1d / §2e). |
| OAuth succeeds then "invalid redirect" | App origin not in Supabase Redirect URLs (§3a). |
| Google "Access blocked: app not verified" | Consent screen still in *Testing* — publish it, or add your email as a test user (§1b.5). |
| Confirmation emails never arrive | Still on built-in sender — set custom SMTP (§3b). |
| "Email address is invalid" | Fake domain (e.g. example.com) — use a real one. |
| Buttons don't appear on prod | Env vars missing or not redeployed (§4.2). |

---

## What Phase 4A deliberately does NOT do yet

Per `AUTH-SPEC.md`, this phase is **sign-in only**. Bookmarks/notes (4B), AI chat
history + per-user rate limiting (4C), and the member tier (4D) are separate
phases. Reading the book and using the chat box remain fully anonymous.
