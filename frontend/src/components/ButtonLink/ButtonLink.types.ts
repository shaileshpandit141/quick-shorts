import IconsMapType from "lazyUtils/LazyIconImport/LazyIconImport.types";

export interface ButtonLinkProps {
  to: string;
  type: 'link' | 'icon';
  icon?: keyof IconsMapType;
  className?: string;
  children?: string;
}
