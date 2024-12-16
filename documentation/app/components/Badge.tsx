import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "bg-neutral-800 text-fd-card-foreground inline-flex rounded-full border-neutral-600 px-4 py-1",
  {
    variants: {
      variant: {
        default:
          "bg-neutral-800 text-fd-card-foreground inline-flex rounded-full border border-neutral-700 px-4 py-1",
        secondary:
          "bg-fd-card text-fd-card-foreground inline-flex rounded-full border border-neutral-600 px-4 py-1",
        destructive:
          "bg-red-200 text-red-800 border border-red-900 inline-flex rounded-full px-4 py-1",
        outline:
          "bg-transparent text-fd-card-foreground border border-white inline-flex rounded-full px-4 py-1",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
