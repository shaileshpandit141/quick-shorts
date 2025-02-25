/**
 * Type declarations for importing SVG files in TypeScript.
 * Allows SVG files to be imported as strings in TypeScript projects.
 */
declare module "*.svg" {
  const content: string;
  export default content;
}

/**
 * Type declarations for importing PNG files in TypeScript.
 * Allows PNG files to be imported as strings in TypeScript projects.
 */
declare module "*.png" {
  const content: string;
  export default content;
}
