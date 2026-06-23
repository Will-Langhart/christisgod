import { SiteHeader } from "@/components/site-header";
import { ReadingProgress } from "@/components/reading-progress";
import { ChapterList } from "@/components/chapter-list";

export default function ReadLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <ReadingProgress />
      <SiteHeader />
      <div className="mx-auto flex w-full max-w-7xl flex-1 gap-10 px-4 sm:px-6">
        {/* Persistent contents sidebar (desktop) */}
        <aside className="hidden w-60 shrink-0 lg:block">
          <div className="sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto py-10 pr-2">
            <ChapterList />
          </div>
        </aside>
        <main className="min-w-0 flex-1">{children}</main>
      </div>
    </>
  );
}
