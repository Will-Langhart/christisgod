-- Phase 4A — Accounts foundation: profiles table.
--
-- One row per auth.users record, created automatically on signup. Holds the
-- membership `role` that later phases gate features/quotas on (never chapter
-- text — see AUTH-SPEC.md §4). RLS restricts every row to its owner; `role` is
-- deliberately NOT self-writable (only the service role may elevate it).

create table if not exists public.profiles (
  id           uuid primary key references auth.users (id) on delete cascade,
  display_name text,
  avatar_url   text,
  role         text not null default 'free' check (role in ('free', 'member', 'admin')),
  created_at   timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- Owner may read their own profile.
create policy "profiles_select_own"
  on public.profiles for select
  using (auth.uid() = id);

-- Owner may update their own profile, but cannot change their role: the WITH
-- CHECK re-reads the row's would-be role and requires it to equal the current
-- stored role. Role changes go through the service role, which bypasses RLS.
create policy "profiles_update_own"
  on public.profiles for update
  using (auth.uid() = id)
  with check (
    auth.uid() = id
    and role = (select p.role from public.profiles p where p.id = auth.uid())
  );

-- Auto-provision a profile whenever a new auth user is created. Pulls a display
-- name / avatar from OAuth metadata when present (Google/Microsoft supply these;
-- email/password signups simply get nulls).
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, display_name, avatar_url)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', new.raw_user_meta_data ->> 'name'),
    new.raw_user_meta_data ->> 'avatar_url'
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
