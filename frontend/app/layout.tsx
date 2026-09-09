import type { ReactNode } from "react";

import "./globals.css";

export const metadata = {
  title: "Weather App",
  description: "Search current weather and save favorite cities",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
