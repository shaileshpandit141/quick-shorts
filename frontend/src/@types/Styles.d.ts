/**
 * Type definitions for CSS modules
 * Allows importing CSS files as modules in TypeScript
 * Each class name in the CSS file becomes a property in the exported object
 */
declare module "*.css" {
  const content: { [className: string]: string };
  export default content;
}
