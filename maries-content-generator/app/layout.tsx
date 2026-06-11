import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Marie's Content Generator",
  description:
    "UGC, Instagram, TikTok, and SWC promo content in Marie's voice — scripts, captions, and upload-ready images.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
