import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';
import { defineConfig } from 'fumadocs-mdx/config';
 
export default defineConfig({
  mdxOptions: {
    remarkPlugins: [remarkMath],
    // Place it at first so that it won't be changed by syntax highlighter
    rehypePlugins: (v) => [rehypeKatex, ...v],
  },
});