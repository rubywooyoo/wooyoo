import { Link, Outlet } from "react-router-dom";

const links = [
  { to: "/admin", label: "總覽" },
  { to: "/admin/campaigns", label: "活動" },
  { to: "/admin/products", label: "商品" },
  { to: "/admin/orders", label: "訂單" },
  { to: "/admin/chat", label: "客服" },
];

export function SellerLayout() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-white/10 bg-black/40 backdrop-blur">
        <div className="mx-auto flex max-w-screen-lg items-center gap-5 px-4 py-4">
          <h1 className="text-lg font-semibold">SnapBuy Admin</h1>
          <nav className="flex gap-4">
            {links.map((link) => (
              <Link key={link.to} to={link.to} className="text-appMuted hover:text-appText">
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-screen-lg px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
