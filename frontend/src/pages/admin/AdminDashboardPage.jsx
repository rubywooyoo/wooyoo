export function AdminDashboardPage() {
  return (
    <section className="space-y-3">
      <h2 className="text-2xl font-semibold">營運總覽</h2>
      <div className="grid gap-3 md:grid-cols-3">
        {["今日營收", "待處理訂單", "熱銷商品"].map((title) => (
          <article key={title} className="rounded-card border border-white/10 bg-appSurface/70 p-4">
            <p className="text-sm text-appMuted">{title}</p>
            <p className="mt-2 text-2xl font-semibold">-</p>
          </article>
        ))}
      </div>
    </section>
  );
}
