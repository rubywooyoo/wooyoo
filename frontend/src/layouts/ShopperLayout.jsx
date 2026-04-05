import { Link, Outlet, useLocation } from "react-router-dom";

const navItems = [
  { to: "/", label: "首頁" },
  { to: "/orders", label: "訂單" },
  { to: "/cart", label: "購物車" },
];

export function ShopperLayout() {
  const location = useLocation();
  return (
    <div className="min-h-screen pb-16">
      <main className="mx-auto max-w-screen-sm px-4 py-4">
        <Outlet />
      </main>
      <nav className="fixed inset-x-0 bottom-0 border-t border-white/10 bg-black/60 backdrop-blur">
        <ul className="mx-auto flex max-w-screen-sm items-center justify-around p-3">
          {navItems.map((item) => (
            <li key={item.to}>
              <Link
                to={item.to}
                className={location.pathname === item.to ? "text-appPrimary" : "text-appMuted"}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
