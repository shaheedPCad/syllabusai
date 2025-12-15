import type { Metadata } from "next";
import { Geist, Geist_Mono, Fraunces } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const fraunces = Fraunces({
  variable: "--font-heading",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "AI Curriculum Designer | Transform Ideas into Standards-Aligned Syllabi",
  description: "Transform vague ideas into comprehensive, standards-aligned syllabi in seconds. Built for educators who value pedagogy over paperwork.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="overflow-x-hidden light">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${fraunces.variable} antialiased overflow-x-hidden bg-white text-foreground`}
      >
        {children}
      </body>
    </html>
  );
}
