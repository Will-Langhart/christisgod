"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";
import { ChapterList } from "@/components/chapter-list";

export function SiteHeader() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-rule bg-parchment/85 backdrop-blur-md">
        <div className="mx-auto flex h-14 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6">
          <div className="flex items-center gap-3">
            <button
              type="button"
              aria-label="Open contents"
              onClick={() => setOpen(true)}
              className="inline-flex h-9 w-9 items-center justify-center rounded-md text-ink-soft hover:text-gold lg:hidden"
            >
              <Menu className="h-5 w-5" />
            </button>
            <Link
              href="/"
              className="flex items-center gap-2 font-[family-name:var(--font-display)] text-lg font-semibold tracking-tight text-ink"
            >
              <span className="text-gold">✠</span>
              <span>Christ Is God</span>
            </Link>
          </div>
          <ThemeToggle />
        </div>
      </header>

      {/* Mobile contents drawer */}
      {open && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setOpen(false)}
          />
          <div className="absolute left-0 top-0 h-full w-[82%] max-w-sm overflow-y-auto border-r border-rule bg-parchment p-5 shadow-2xl">
            <div className="mb-4 flex items-center justify-between">
              <span className="font-[family-name:var(--font-display)] text-lg font-semibold text-ink">
                <span className="text-gold">✠</span> Christ Is God
              </span>
              <button
                type="button"
                aria-label="Close contents"
                onClick={() => setOpen(false)}
                className="inline-flex h-9 w-9 items-center justify-center rounded-md text-ink-soft hover:text-gold"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <ChapterList onNavigate={() => setOpen(false)} />
          </div>
        </div>
      )}
    </>
  );
}
