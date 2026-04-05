import { motion } from "framer-motion";
import { useParams } from "react-router-dom";

export function StoryPage() {
  const { campaignId } = useParams();
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-semibold">沉浸式限動 / 活動 #{campaignId}</h2>
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-hero border border-white/10 bg-appSurface/70 p-5"
      >
        <div className="h-[56vh] rounded-hero bg-white/10" />
        <div className="mt-4 flex gap-2">
          <button className="rounded-card border border-white/20 px-3 py-2 text-sm">回覆此商品</button>
          <button className="rounded-card border border-white/20 px-3 py-2 text-sm">收藏</button>
          <button className="rounded-card bg-appPrimary px-3 py-2 text-sm text-black">加入購物車</button>
        </div>
      </motion.div>
    </section>
  );
}
