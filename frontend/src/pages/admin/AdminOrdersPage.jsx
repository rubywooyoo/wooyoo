export function AdminOrdersPage() {
  return (
    <section className="space-y-3">
      <h2 className="text-2xl font-semibold">訂單管理</h2>
      <div className="rounded-card border border-white/10 bg-appSurface/70 p-4">
        <p className="text-sm text-appMuted">Kanban 欄位：待付款、已付款、待出貨、已出貨。</p>
      </div>
    </section>
  );
}
