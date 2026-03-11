import { ButtonHTMLAttributes, ReactNode } from "react";

import { cn } from "@/lib/utils";

export function Panel({
  children,
  className,
  title,
  eyebrow,
}: {
  children: ReactNode;
  className?: string;
  title?: string;
  eyebrow?: string;
}) {
  return (
    <section className={cn("rounded-3xl border border-line bg-panel p-6 shadow-panel", className)}>
      {(eyebrow || title) && (
        <header className="mb-4">
          {eyebrow && <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted">{eyebrow}</p>}
          {title && <h2 className="mt-1 text-lg font-semibold text-ink">{title}</h2>}
        </header>
      )}
      {children}
    </section>
  );
}

export function MetricCard({ label, value, tone = "default" }: { label: string; value: string | number; tone?: "default" | "warning" | "danger" }) {
  const toneClasses = {
    default: "border-line",
    warning: "border-warning/30 bg-warning/5",
    danger: "border-danger/30 bg-danger/5",
  };
  return (
    <div className={cn("rounded-2xl border p-4", toneClasses[tone])}>
      <p className="text-sm text-muted">{label}</p>
      <p className="mt-2 text-3xl font-semibold">{value}</p>
    </div>
  );
}

export function StatusPill({ label, tone }: { label: string; tone?: "success" | "warning" | "danger" | "neutral" }) {
  const toneClasses = {
    success: "bg-accent/10 text-accent",
    warning: "bg-warning/10 text-warning",
    danger: "bg-danger/10 text-danger",
    neutral: "bg-slate-200 text-slate-700",
  };
  return <span className={cn("rounded-full px-3 py-1 text-xs font-semibold capitalize", toneClasses[tone ?? "neutral"])}>{label}</span>;
}

export function Button({
  children,
  className,
  variant = "primary",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" }) {
  const variants = {
    primary: "bg-ink text-white hover:bg-slate-800",
    secondary: "bg-bg text-ink hover:bg-slate-200",
  };
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-2xl px-4 py-3 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
