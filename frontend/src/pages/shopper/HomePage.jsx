import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-semibold">買家首頁</h2>
      <div className="rounded-hero border border-white/10 bg-appSurface/60 p-4">
        <p className="text-sm text-appMuted">限動圈圈（Story Bubbles）</p>
        <div className="mt-3 flex gap-3 overflow-x-auto">
          {["韓國連線", "日本藥妝", "歐美服飾"].map((name) => (
            <Link
              key={name}
              to="/story/1"
              className="min-w-20 rounded-full border border-appPrimary/70 px-3 py-5 text-center text-xs"
            >
              {name}
            </Link>
          ))}
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="rounded-card border border-white/10 bg-appSurface/70 p-3">
            <div className="h-28 rounded-card bg-white/10" />
            <p className="mt-2 text-sm">商品 {i}</p>
            <p className="text-xs text-appPrimary">剩餘 01:23:45</p>
          </div>
        ))}
      </div>
    </section>
  );
}
