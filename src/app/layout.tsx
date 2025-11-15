import type { Metadata } from "next";
import "./globals.css";
import "easymde/dist/easymde.min.css";

export const metadata: Metadata = {
  title: "Journal App",
  description: "A beautiful, simple journaling application with markdown support",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
