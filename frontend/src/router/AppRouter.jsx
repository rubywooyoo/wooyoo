import { Route, Routes } from "react-router-dom";

import { SellerLayout } from "../layouts/SellerLayout";
import { ShopperLayout } from "../layouts/ShopperLayout";
import { AdminChatPage } from "../pages/admin/AdminChatPage";
import { AdminDashboardPage } from "../pages/admin/AdminDashboardPage";
import { AdminOrdersPage } from "../pages/admin/AdminOrdersPage";
import { CampaignsPage } from "../pages/admin/CampaignsPage";
import { ProductsPage } from "../pages/admin/ProductsPage";
import { CartPage } from "../pages/shopper/CartPage";
import { HomePage } from "../pages/shopper/HomePage";
import { OrdersPage } from "../pages/shopper/OrdersPage";
import { StoryPage } from "../pages/shopper/StoryPage";

export function AppRouter() {
  return (
    <Routes>
      <Route element={<ShopperLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/story/:campaignId" element={<StoryPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/orders" element={<OrdersPage />} />
      </Route>

      <Route path="/admin" element={<SellerLayout />}>
        <Route index element={<AdminDashboardPage />} />
        <Route path="campaigns" element={<CampaignsPage />} />
        <Route path="products" element={<ProductsPage />} />
        <Route path="orders" element={<AdminOrdersPage />} />
        <Route path="chat" element={<AdminChatPage />} />
      </Route>
    </Routes>
  );
}
