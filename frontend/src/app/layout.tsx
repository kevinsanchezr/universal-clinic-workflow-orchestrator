import type { Metadata } from "next";
import type { ReactNode } from "react";

import { Providers } from "@/components/providers";
import { Sidebar } from "@/components/sidebar";

import "./globals.css";


export const metadata: Metadata = {
  title: "Universal Clinic Workflow Orchestrator",
  description: "Operational reliability layer for clinic AI employees.",
};


export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[280px_1fr]">
            <Sidebar />
            <main className="p-6 lg:p-10">{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
