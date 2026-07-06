import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ContentForge",
  description:
    "UGC, Instagram, TikTok, and digital-product promo content in your voice — scripts, captions, and upload-ready images.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
