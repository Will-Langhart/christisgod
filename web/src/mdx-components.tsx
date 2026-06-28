import type { MDXComponents } from "mdx/types";
import type { AnchorHTMLAttributes } from "react";
import { ScriptureRef } from "@/components/scripture-ref";
import {
  KeyTakeaways,
  WordStudy,
  PullQuote,
  SeeAlso,
} from "@/components/enrichment";

type AnchorProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  "data-ref"?: string;
  dataRef?: string;
};

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    KeyTakeaways,
    WordStudy,
    PullQuote,
    SeeAlso,
    a: ({ className, children, ...props }: AnchorProps) => {
      const classes = Array.isArray(className) ? className.join(" ") : className;
      if (classes?.includes("scripture-ref")) {
        const ref = props["data-ref"] ?? props.dataRef;
        return <ScriptureRef dataRef={ref}>{children}</ScriptureRef>;
      }
      return (
        <a className={classes} {...props}>
          {children}
        </a>
      );
    },
  };
}
